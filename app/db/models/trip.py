from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Trip(Base):
    __tablename__ = "trip"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finish_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id", ondelete="SET NULL"))
    vehicle: Mapped["Vehicle"] = relationship(back_populates="trips")  # noqa F821 # type: ignore
