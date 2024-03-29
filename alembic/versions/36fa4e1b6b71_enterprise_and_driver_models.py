"""Enterprise and Driver models

Revision ID: 36fa4e1b6b71
Revises: f6be6032a03b
Create Date: 2024-02-01 10:00:51.080158

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "36fa4e1b6b71"
down_revision: Union[str, None] = "f6be6032a03b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "enterprise",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("company_name", sa.String(), nullable=False),
        sa.Column("company_address", sa.String(), nullable=False),
        sa.Column("contact_email", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_enterprise_id"), "enterprise", ["id"], unique=False)
    op.create_table(
        "driver",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("salary", sa.BigInteger(), nullable=True),
        sa.Column("enterpise_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["enterpise_id"], ["enterprise.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_driver_id"), "driver", ["id"], unique=False)
    op.add_column("vehicle", sa.Column("enterpise_id", sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, "vehicle", "enterprise", ["enterpise_id"], ["id"], ondelete="SET NULL")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "vehicle", type_="foreignkey")
    op.drop_column("vehicle", "enterpise_id")
    op.drop_index(op.f("ix_driver_id"), table_name="driver")
    op.drop_table("driver")
    op.drop_index(op.f("ix_enterprise_id"), table_name="enterprise")
    op.drop_table("enterprise")
    # ### end Alembic commands ###
