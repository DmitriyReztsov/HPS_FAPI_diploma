"""add cascade delete in VehicleModel model

Revision ID: f6be6032a03b
Revises: be705f3c420d
Create Date: 2024-01-29 20:41:08.450154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f6be6032a03b"
down_revision: Union[str, None] = "be705f3c420d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("vehiclemodel_brand_id_fkey", "vehiclemodel", type_="foreignkey")
    op.create_foreign_key(None, "vehiclemodel", "vehiclebrand", ["brand_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "vehiclemodel", type_="foreignkey")
    op.create_foreign_key("vehiclemodel_brand_id_fkey", "vehiclemodel", "vehiclebrand", ["brand_id"], ["id"])
    # ### end Alembic commands ###