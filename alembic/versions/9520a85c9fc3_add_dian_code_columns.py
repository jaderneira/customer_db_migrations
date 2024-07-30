"""add dian_code columns

Revision ID: 9520a85c9fc3
Revises: 86d8d519a41a
Create Date: 2024-06-28 16:35:49.974380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9520a85c9fc3'
down_revision = '86d8d519a41a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'general_countries',
        sa.Column("dian_code", sa.String(3), unique=True, nullable=True),
    )
    op.add_column(
        'general_countries',
        sa.Column("code", sa.String(2), unique=True, nullable=True),
    )
    op.add_column(
        'general_cities',
        sa.Column("dian_code", sa.String(3), unique=True, nullable=True),
    )
    op.add_column(
        'general_cities',
        sa.Column("department_id", sa.Integer, sa.ForeignKey("general_departments.department_id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('general_countries', 'dian_code')
    op.drop_column('general_cities', 'dian_code')
    op.drop_column('general_countries', 'code')
    op.drop_column('general_cities', 'department_id')