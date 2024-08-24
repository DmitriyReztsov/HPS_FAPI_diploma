"""Add relations report with enterprise

Revision ID: 057e3b8b04a4
Revises: 4699f3fbef57
Create Date: 2024-07-11 17:20:11.087864

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "057e3b8b04a4"
down_revision: Union[str, None] = "4699f3fbef57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("report", sa.Column("enterprise_id", sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, "report", "enterprise", ["enterprise_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(None, "report", type_="foreignkey")
    op.drop_column("report", "enterprise_id")
