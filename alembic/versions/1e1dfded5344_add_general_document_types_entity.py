"""add general_document_types entity

Revision ID: 1e1dfded5344
Revises: 
Create Date: 2024-01-11 21:59:22.773056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e1dfded5344'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "general_document_types",
        sa.Column("document_type_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(32), unique=True, nullable=False),
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
        CREATE OR REPLACE FUNCTION set_timestamp() RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER set_timestamp_trigger
        BEFORE UPDATE ON general_document_types
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
                               
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON general_document_types;

        DROP FUNCTION IF EXISTS set_timestamp;
    """))

    op.drop_table("general_document_types")
