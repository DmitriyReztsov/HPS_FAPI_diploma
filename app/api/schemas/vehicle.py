from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    brandmodel_id: int
    description: str
    cost: int
    manufactured_year: int
    mileage: int
    is_in_work: bool | None = True

    class Config:
        from_attributes = True


class VehicleFromDB(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
