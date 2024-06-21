from datetime import datetime
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class VehicleBrand(Base):
    __tablename__ = "vehiclebrand"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    brand_name: Mapped[str] = mapped_column(nullable=False)
    original_country: Mapped[str] = mapped_column(nullable=False)

    models: Mapped[list["VehicleModel"]] = relationship(back_populates="brand")

    def __str__(self):
        return self.brand_name


class VehicleModel(Base):
    __tablename__ = "vehiclemodel"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    exact_model_name: Mapped[str] = mapped_column(nullable=True)
    vehicle_type: Mapped[str] = mapped_column(nullable=False)  # add choices
    passenger_capacity: Mapped[int] = mapped_column(nullable=False)
    tonnage: Mapped[int] = mapped_column(nullable=False)
    fuel_capacity: Mapped[int] = mapped_column(nullable=False)

    brand_id: Mapped[int] = mapped_column(ForeignKey("vehiclebrand.id", ondelete="CASCADE"))
    brand: Mapped[Optional["VehicleBrand"]] = relationship(back_populates="models", lazy="joined")

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="brandmodel")

    def __str__(self):
        return f"{self.brand.brand_name} {self.exact_model_name}"


class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    cost: Mapped[int] = mapped_column(BigInteger, nullable=True)
    manufactured_year: Mapped[int] = mapped_column(nullable=False)
    purchase_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    mileage: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_in_work: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    brandmodel_id: Mapped[int] = mapped_column(ForeignKey("vehiclemodel.id", ondelete="SET NULL"), nullable=True)
    brandmodel: Mapped[Optional["VehicleModel"]] = relationship(back_populates="vehicles", lazy="immediate")

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprise.id", ondelete="SET NULL"), nullable=True)
    enterprise: Mapped["Enterprise"] = relationship(  # noqa F821 # type: ignore
        "Enterprise", back_populates="vehicles", lazy="joined"
    )

    drivers: Mapped[list["DriverVehicle"]] = relationship(  # noqa F821 # type: ignore
        "DriverVehicle", back_populates="vehicle"
    )

    trackpoints: Mapped[list["VehicleTrackPoint"]] = relationship(back_populates="vehicle")

    def __str__(self) -> str:
        return f"{self.id} {'OK' if self.is_in_work else 'NOK'}"


class VehicleTrackPoint(Base):
    __tablename__ = "vehicletrackpoint"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    geotag: Mapped[list[float]] = mapped_column(Geometry("POINT"))

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id", ondelete="CASCADE"), nullable=False)
    vehicle: Mapped[Optional["Vehicle"]] = relationship(back_populates="trackpoints", lazy="immediate")

    @property
    def repr_geotag(self) -> str:
        return "To be implemented..."
