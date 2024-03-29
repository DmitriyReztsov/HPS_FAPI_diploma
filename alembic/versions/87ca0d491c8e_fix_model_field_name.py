"""fix model field name

Revision ID: 87ca0d491c8e
Revises: deeda98edac0
Create Date: 2024-01-25 22:39:56.251699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "87ca0d491c8e"
down_revision: Union[str, None] = "deeda98edac0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("vehiclemodel", sa.Column("exact_model_name", sa.String(), nullable=True))
    op.drop_column("vehiclemodel", "model_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("vehiclemodel", sa.Column("model_name", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column("vehiclemodel", "exact_model_name")
    # ### end Alembic commands ###
