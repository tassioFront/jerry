"""add user type

Revision ID: c23f2794cb67
Revises: 003_create_outbox_event_table
Create Date: 2025-12-16 14:42:10.899690
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c23f2794cb67"
down_revision: Union[str, None] = "003_create_outbox_event_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- outbox_event indexes ---
    op.drop_index("idx_outbox_event_aggregate_id", table_name="outbox_event")
    op.drop_index("idx_outbox_event_event_type", table_name="outbox_event")
    op.drop_index("idx_outbox_event_status_occurred_at", table_name="outbox_event")

    op.create_index(
        op.f("ix_outbox_event_aggregate_id"),
        "outbox_event",
        ["aggregate_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_outbox_event_event_type"),
        "outbox_event",
        ["event_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_outbox_event_id"),
        "outbox_event",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_outbox_event_status"),
        "outbox_event",
        ["status"],
        unique=False,
    )

    # --- user.type enum + column ---
    user_type_enum = sa.Enum(
        "SUDO",
        "ADMIN",
        "AUDIT",
        "CLIENT",
        name="user_type_enum",
    )
    # create underlying enum type in Postgres
    user_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "user",
        sa.Column("type", user_type_enum, nullable=False),
    )

    # --- user indexes ---
    op.drop_index("idx_user_created_at", table_name="user")
    op.drop_index("idx_user_email", table_name="user")
    op.drop_constraint("user_email_key", "user", type_="unique")

    op.create_index(
        op.f("ix_user_email"),
        "user",
        ["email"],
        unique=True,
    )
    op.create_index(
        op.f("ix_user_id"),
        "user",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_type"),
        "user",
        ["type"],
        unique=False,
    )


def downgrade() -> None:
    # --- user indexes ---
    op.drop_index(op.f("ix_user_type"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")

    op.create_unique_constraint("user_email_key", "user", ["email"])
    op.create_index(
        "idx_user_email",
        "user",
        ["email"],
        unique=False,
    )
    op.create_index(
        "idx_user_created_at",
        "user",
        ["created_at"],
        unique=False,
    )

    # --- user.type enum + column ---
    op.drop_column("user", "type")

    user_type_enum = sa.Enum(
        "SUDO",
        "ADMIN",
        "AUDIT",
        "CLIENT",
        name="user_type_enum",
    )
    user_type_enum.drop(op.get_bind(), checkfirst=True)

    # --- outbox_event indexes ---
    op.drop_index(op.f("ix_outbox_event_status"), table_name="outbox_event")
    op.drop_index(op.f("ix_outbox_event_id"), table_name="outbox_event")
    op.drop_index(op.f("ix_outbox_event_event_type"), table_name="outbox_event")
    op.drop_index(op.f("ix_outbox_event_aggregate_id"), table_name="outbox_event")

    op.create_index(
        "idx_outbox_event_status_occurred_at",
        "outbox_event",
        ["status", "occurred_at"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_event_event_type",
        "outbox_event",
        ["event_type"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_event_aggregate_id",
        "outbox_event",
        ["aggregate_id"],
        unique=False,
    )
