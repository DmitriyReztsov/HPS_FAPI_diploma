"""reports models

Revision ID: 4699f3fbef57
Revises: 613bd5e7c184
Create Date: 2024-07-07 21:22:15.067667

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4699f3fbef57"
down_revision: Union[str, None] = "613bd5e7c184"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "report",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column(
            "period", sa.Enum("DAILY", "MONTHLY", "QUARTERLY", "ANNUALLY", name="reportperiodchoices"), nullable=False
        ),
        sa.Column("from_date", sa.Date(), nullable=False),
        sa.Column("to_date", sa.Date(), nullable=False),
        sa.Column("report_result", sa.JSON(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vehiclemileagereport",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["report.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vehiclemileagereport")
    op.drop_table("report")
    # ### end Alembic commands ###
