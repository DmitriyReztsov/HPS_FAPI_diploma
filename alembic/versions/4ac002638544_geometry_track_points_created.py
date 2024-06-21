"""Geometry track points created

Revision ID: 4ac002638544
Revises: 70de8139a2ee
Create Date: 2024-05-25 18:51:11.111408

"""

from typing import Sequence, Union

from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4ac002638544"
down_revision: Union[str, None] = "70de8139a2ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vehicletrackpoint",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("date_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "geotag",
            geoalchemy2.types.Geometry(
                geometry_type="POINT", from_text="ST_GeomFromEWKT", name="geometry", nullable=False
            ),
            nullable=False,
        ),
        sa.Column("vehicle_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicle.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_vehicletrackpoint_geotag", table_name="vehicletrackpoint", postgresql_using="gist")
    op.drop_table("vehicletrackpoint")
    # ### end Alembic commands ###
