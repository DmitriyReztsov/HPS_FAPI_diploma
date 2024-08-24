from datetime import date

from pydantic import BaseModel, ConfigDict


class ReportCreateRequest(BaseModel):
    vehicle_id: int
    title: str | None = None
    period: str
    from_date: date
    to_date: date
    type: str
    enterprise_id: int | None = None


class ReportCreate(BaseModel):
    title: str | None = None
    period: str
    from_date: date
    to_date: date
    type: str
    report_result: dict
    enterprise_id: int | None = None

    class Config:
        from_attributes = True


class ReportFromDB(ReportCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
