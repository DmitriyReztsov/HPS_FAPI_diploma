from sqlalchemy import BigInteger
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.associations import manager_enterprise_association_table


class Manager(Base):
    __tablename__ = "manager"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    enterprises: Mapped[list["Enterprise"]] = relationship(  # noqa F821 # type: ignore
        "Enterprise", secondary=manager_enterprise_association_table, back_populates="managers"
    )

    def __str__(self):
        return self.get_full_name

    @hybrid_property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
