"""add company_details entity

Revision ID: 691207aedf92
Revises: 15f39da3c5ce
Create Date: 2024-01-11 23:44:54.797201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '691207aedf92'
down_revision = '15f39da3c5ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "company_details",
        sa.Column("company_detail_id", sa.UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("document_type_id", sa.Integer, sa.ForeignKey("general_document_types.document_type_id"), nullable=False),
        sa.Column("company_id", sa.UUID, sa.ForeignKey("companies.company_id"), nullable=False),
        sa.Column("broker_id", sa.UUID, sa.ForeignKey("companies.company_id")),
        sa.Column("is_broker", sa.Boolean, default=False),        
        sa.Column("identification", sa.String(64), unique=True, nullable=False),
        sa.Column("poc_name", sa.String(64)),       
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
        BEFORE UPDATE ON company_details
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON company_details;
    """))

    op.drop_table("company_details")
