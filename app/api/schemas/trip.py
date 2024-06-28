from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TripCreate(BaseModel):
    start_date_time: datetime
    finish_date_time: datetime
    vehicle_id: int

    class Config:
        from_attributes = True


class TripFromDB(TripCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
