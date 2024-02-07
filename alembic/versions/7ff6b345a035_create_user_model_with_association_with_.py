"""create User model with association with Enterprise

Revision ID: 7ff6b345a035
Revises: 71335498f67a
Create Date: 2024-02-06 10:58:01.282389

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7ff6b345a035"
down_revision: Union[str, None] = "71335498f67a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "user_enterprise_association_table",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("enterprise_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["enterprise_id"],
            ["enterprise.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "enterprise_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_enterprise_association_table")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###