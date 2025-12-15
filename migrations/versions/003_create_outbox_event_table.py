"""Create outbox_event table for transactional outbox pattern.

Revision ID: 003_create_outbox_event_table
Revises: 002_add_user_name_fields
Create Date: 2024-01-17 10:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "003_create_outbox_event_table"
down_revision: Union[str, None] = "002_add_user_name_fields"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create outbox_event table."""
    op.create_table(
        "outbox_event",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("event_type", sa.String(255), nullable=False),
        sa.Column("aggregate_id", sa.String(255), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.create_index(
        "idx_outbox_event_status_occurred_at",
        "outbox_event",
        ["status", "occurred_at"],
    )
    op.create_index(
        "idx_outbox_event_event_type",
        "outbox_event",
        ["event_type"],
    )
    op.create_index(
        "idx_outbox_event_aggregate_id",
        "outbox_event",
        ["aggregate_id"],
    )


def downgrade() -> None:
    """Drop outbox_event table."""
    op.drop_index("idx_outbox_event_aggregate_id", table_name="outbox_event")
    op.drop_index("idx_outbox_event_event_type", table_name="outbox_event")
    op.drop_index("idx_outbox_event_status_occurred_at", table_name="outbox_event")
    op.drop_table("outbox_event")


