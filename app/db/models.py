from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    cost: Mapped[int] = mapped_column(BigInteger, nullable=True)
    manufactured_year: Mapped[int] = mapped_column(nullable=False)
    mileage: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_in_work: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
