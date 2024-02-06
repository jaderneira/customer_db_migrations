"""add orders entity

Revision ID: c3a0290470a1
Revises: 691207aedf92
Create Date: 2024-01-26 22:09:48.382644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3a0290470a1'
down_revision = '691207aedf92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "orders",
        sa.Column("order_id", sa.UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("company_id", sa.UUID, sa.ForeignKey("companies.company_id"), nullable=False),
        sa.Column("importer_id", sa.UUID, sa.ForeignKey("companies.company_id"), nullable=False),
        sa.Column("provider_id", sa.UUID, sa.ForeignKey("companies.company_id"), nullable=False),
        sa.Column("landing_stage_id", sa.Integer, sa.ForeignKey("general_landing_stages.landing_stage_id"), nullable=False),
        sa.Column("shipping_lane_id", sa.Integer, sa.ForeignKey("general_shipping_lanes.shipping_lane_id"), nullable=False),
        sa.Column("order_status_id", sa.Integer, sa.ForeignKey("general_order_statuses.order_status_id"), nullable=True),
        sa.Column("type", sa.String(8), nullable=False),
        sa.Column("estimated_time_arrival", sa.Date),
        sa.Column("do_number", sa.String(64)),
        sa.Column("do_company_number", sa.String(64)),
        sa.Column("digitizer_name", sa.String(32)),
        sa.Column("description", sa.Text),
        sa.Column("bl_number", sa.String(64)),
        sa.Column("motorboat", sa.String(32)),
        sa.Column("container_number", sa.String(128)),
        sa.Column("document_type", sa.String(32)),
        sa.Column("bl_broadcast_type", sa.String(32)),
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
        BEFORE UPDATE ON orders
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON orders;
    """))

    op.drop_table("orders")

