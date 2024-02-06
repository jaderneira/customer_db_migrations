"""add general_cities entity

Revision ID: 09298fbff07c
Revises: 81b5ae92af07
Create Date: 2024-01-11 22:49:27.981187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09298fbff07c'
down_revision = '81b5ae92af07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "general_cities",
        sa.Column("city_id", sa.Integer, primary_key=True),
        sa.Column("country_id", sa.Integer, sa.ForeignKey("general_countries.country_id"), nullable=False),
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
        BEFORE UPDATE ON general_cities
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON general_cities;
    """))

    op.drop_table("general_cities")
