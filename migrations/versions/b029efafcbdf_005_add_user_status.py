"""005_add_user_status

Revision ID: b029efafcbdf
Revises: c23f2794cb67
Create Date: 2025-12-17 16:57:29.125680
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision = 'b029efafcbdf'
down_revision = 'c23f2794cb67'
branch_labels = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create enum type first
    user_status_enum = sa.Enum('active', 'deactivated', 'blocked', name='user_status_enum')
    user_status_enum.create(op.get_bind())
    
    # Add column with default for existing rows
    op.add_column('user', sa.Column('status', user_status_enum, server_default='active', nullable=False))

def downgrade() -> None:
    # Drop column first
    op.drop_column('user', 'status')
    # Drop enum type
    user_status_enum = sa.Enum('active', 'deactivated', 'blocked', name='user_status_enum')
    user_status_enum.drop(op.get_bind())
