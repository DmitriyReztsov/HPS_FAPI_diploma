from pydantic import BaseModel, ConfigDict

from app.api.schemas.driver import DriverFromDB
from app.api.schemas.vehicle import VehicleFromDB


class EnterpriseCreate(BaseModel):
    company_name: str
    company_address: str
    contact_email: str

    class Config:
        from_attributes = True


class EnterpriseFromDB(EnterpriseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicles: list[VehicleFromDB]
    drivers: list[DriverFromDB]
