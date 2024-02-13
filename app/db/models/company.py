from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.models.associations import user_enterprise_association_table


class Enterprise(Base):
    __tablename__ = "enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(nullable=False)
    company_address: Mapped[str] = mapped_column(nullable=False)
    contact_email: Mapped[str] = mapped_column(nullable=False)

    vehicles: Mapped[list["Vehicle"]] = relationship(  # noqa F821 # type: ignore
        "Vehicle", back_populates="enterprise", lazy="immediate"
    )
    drivers: Mapped[list["Driver"]] = relationship(  # noqa F821 # type: ignore
        "Driver", back_populates="enterprise", uselist=True, lazy="immediate"
    )

    users: Mapped[list["User"]] = relationship(  # noqa F821 # type: ignore
        "User", secondary=user_enterprise_association_table, back_populates="enterprises", lazy="immediate"
    )

    def __str__(self):
        return self.company_name
