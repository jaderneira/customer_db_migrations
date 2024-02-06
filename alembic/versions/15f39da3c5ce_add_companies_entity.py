"""add companies entity

Revision ID: 15f39da3c5ce
Revises: 09298fbff07c
Create Date: 2024-01-11 22:55:32.256559

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '15f39da3c5ce'
down_revision = '09298fbff07c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "companies",
        sa.Column("company_id", sa.UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("company_type_id", sa.Integer, sa.ForeignKey("general_company_types.company_type_id")),
        sa.Column("city_id", sa.Integer, sa.ForeignKey("general_cities.city_id")),
        sa.Column("name", sa.String(128), unique=True, nullable=False),
        sa.Column("address", sa.Text),
        sa.Column("email", sa.String(64)),
        sa.Column("phone", sa.String(32)),
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
        BEFORE UPDATE ON companies
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON companies;
    """))

    op.drop_table("companies")
