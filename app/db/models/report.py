from datetime import date
from enum import Enum

from sqlalchemy import BigInteger, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db.database import Base


ReportPeriodChoices = Enum(
    "ReportPeriodChoices",
    {
        "DAILY": "daily",
        "MONTHLY": "monthly",
        "QUARTERLY": "quarterly",
        "ANNUALLY": "annually",
    },
)


class Report(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column()
    period: Mapped[ReportPeriodChoices] = mapped_column()
    from_date: Mapped[date] = mapped_column(Date())
    to_date: Mapped[date] = mapped_column(Date())
    report_result: Mapped[dict] = mapped_column(type_=JSON)

    type: Mapped[str]

    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprise.id", ondelete="CASCADE"), nullable=True)
    enterprise: Mapped["Enterprise"] = relationship(  # noqa F821 # type: ignore
        "Enterprise", back_populates="reports", lazy="joined"
    )

    __mapper_args__ = {
        "polymorphic_identity": "report",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


class VehicleMileageReport(Report):
    __tablename__ = "vehiclemileagereport"

    id: Mapped[int] = mapped_column(ForeignKey("report.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "vehiclemileagereport",
    }
