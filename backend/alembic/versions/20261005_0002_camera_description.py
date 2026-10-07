"""Add the documented optional camera description."""

from alembic import op
import sqlalchemy as sa


revision = "20261005_0002"
down_revision = "20260912_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cameras", sa.Column("description", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("cameras", "description")
