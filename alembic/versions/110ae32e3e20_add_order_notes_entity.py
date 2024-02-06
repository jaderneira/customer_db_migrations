"""add order_notes entity

Revision ID: 110ae32e3e20
Revises: c3a0290470a1
Create Date: 2024-01-26 22:28:09.612596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '110ae32e3e20'
down_revision = 'c3a0290470a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()

    op.create_table(
        "order_notes",
        sa.Column("order_note_id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.UUID, sa.ForeignKey("orders.order_id"), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("created_by", sa.String(32)),
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
        BEFORE UPDATE ON order_notes
        FOR EACH ROW EXECUTE PROCEDURE set_timestamp();
    """))


def downgrade() -> None:
    connection = op.get_bind()

    # Delete trigger
    connection.execute(sa.text("""
        DROP TRIGGER IF EXISTS set_timestamp_trigger ON order_notes;
    """))

    op.drop_table("order_notes")
