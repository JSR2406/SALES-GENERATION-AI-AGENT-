"""add_agent_logs_table

Revision ID: cba2309a0621
Revises: c34df6d933d0
Create Date: 2026-03-13 19:02:27.389951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cba2309a0621'
down_revision: Union[str, None] = 'c34df6d933d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('agent_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('campaign_id', sa.UUID(), nullable=False),
        sa.Column('node', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_agent_logs'))
    )

def downgrade() -> None:
    op.drop_table('agent_logs')
