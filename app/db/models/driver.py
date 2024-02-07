# from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Driver(Base):
    __tablename__ = "driver"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[int] = mapped_column(BigInteger, nullable=True)

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprise.id", ondelete="SET NULL"), nullable=True)
    enterprise: Mapped["Enterprise"] = relationship("Enterprise", back_populates="drivers")  # noqa F821 # type: ignore

    vehicles: Mapped[list["DriverVehicle"]] = relationship("DriverVehicle", back_populates="driver", lazy="immediate")

    def __str__(self):
        return self.get_full_name

    @hybrid_property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class DriverVehicle(Base):
    __tablename__ = "drivervehicle"

    is_active_driver: Mapped[bool] = mapped_column(default=False)

    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id", ondelete="CASCADE"), primary_key=True)
    driver: Mapped["Driver"] = relationship("Driver", back_populates="vehicles", lazy="immediate")

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id", ondelete="CASCADE"), primary_key=True)
    vehicle: Mapped["Vehicle"] = relationship(  # noqa F821 # type: ignore
        "Vehicle", back_populates="drivers", lazy="immediate"
    )

    def __str__(self) -> str:
        return f"{self.driver} on {self.vehicle}"
