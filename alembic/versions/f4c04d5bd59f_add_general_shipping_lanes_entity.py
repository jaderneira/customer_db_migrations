"""add general_shipping_lanes entity

Revision ID: f4c04d5bd59f
Revises: 0789f5f95fcb
Create Date: 2024-01-11 22:38:00.274855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4c04d5bd59f'
down_revision = '0789f5f95fcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
# text

    op.create_table(
        "general_shipping_lanes",
        sa.Column("shipping_lane_id", sa.Integer, primary_key=True),
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
        BEFORE UPDATE ON general_shipping_lanes
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON general_shipping_lanes;
    """))

    op.drop_table("general_shipping_lanes")
