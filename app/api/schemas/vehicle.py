from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    brandmodel_id: int
    description: str
    cost: int
    manufactured_year: int
    mileage: int
    is_in_work: bool | None = True
    enterprise_id: int | None = None

    class Config:
        from_attributes = True


class VehiclePartialUpdate(BaseModel):
    brandmodel_id: int | None = None
    description: str | None = None
    cost: int | None = None
    manufactured_year: int | None = None
    mileage: int | None = None
    is_in_work: bool | None = None
    enterprise_id: int | None = None


class VehicleFromDB(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
