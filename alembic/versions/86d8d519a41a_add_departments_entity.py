"""add departments entity

Revision ID: 86d8d519a41a
Revises: b49044f79571
Create Date: 2024-06-28 15:24:17.306016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86d8d519a41a'
down_revision = 'b49044f79571'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "general_departments",
        sa.Column("department_id", sa.Integer, primary_key=True),
        sa.Column("country_id", sa.Integer, sa.ForeignKey("general_countries.country_id"), nullable=False),
        sa.Column("name", sa.String(64), unique=True, nullable=False),
        sa.Column("dian_code", sa.String(2), unique=True, nullable=True),
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
        BEFORE UPDATE ON general_departments
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON general_departments;
    """))

    op.drop_table("general_departments")

