"""add color column to general_order_statuses entity

Revision ID: b49044f79571
Revises: 110ae32e3e20
Create Date: 2024-02-05 18:32:35.901513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b49044f79571'
down_revision = '110ae32e3e20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'general_order_statuses',
        sa.Column("color", sa.String(32)),
    )


def downgrade() -> None:
    op.drop_column('general_order_statuses', 'color')
