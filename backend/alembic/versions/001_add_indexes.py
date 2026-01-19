"""Add indexes for conversation and message tables

Revision ID: 001_add_indexes
Revises:
Create Date: 2026-01-19 04:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '001_add_indexes'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create indexes for better query performance
    op.create_index('idx_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('idx_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('idx_message_timestamp', 'message', ['timestamp'])
    op.create_index('idx_message_role', 'message', ['role'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_conversation_user_id', table_name='conversation')
    op.drop_index('idx_message_conversation_id', table_name='message')
    op.drop_index('idx_message_timestamp', table_name='message')
    op.drop_index('idx_message_role', table_name='message')