"""add Trip model

Revision ID: 613bd5e7c184
Revises: 4ac002638544
Create Date: 2024-06-26 10:51:43.519298

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "613bd5e7c184"
down_revision: Union[str, None] = "4ac002638544"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "trip",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("start_date_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finish_date_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("vehicle_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicle.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("trip")
