"""add general_order_statuses entity

Revision ID: 4e04ebddcc3e
Revises: f4c04d5bd59f
Create Date: 2024-01-11 22:40:20.630176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e04ebddcc3e'
down_revision = 'f4c04d5bd59f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "general_order_statuses",
        sa.Column("order_status_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(64), unique=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime,
            nullable=True,
        ),
    )

    connection.execute(sa.text("""
        CREATE TRIGGER set_timestamp_trigger
        BEFORE UPDATE ON general_order_statuses
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON general_order_statuses;
    """))

    op.drop_table("general_order_statuses")
