"""add general_landing_stages entity

Revision ID: 0789f5f95fcb
Revises: bfe12e458d3a
Create Date: 2024-01-11 22:36:19.412031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0789f5f95fcb'
down_revision = 'bfe12e458d3a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "general_landing_stages",
        sa.Column("landing_stage_id", sa.Integer, primary_key=True),
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
        BEFORE UPDATE ON general_landing_stages
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON general_landing_stages;
    """))

    op.drop_table("general_landing_stages")
