from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.api.schemas.vehicle_model import VehicleModelFromDB

# from app.api.schemas.enterprise import EnterpriseShort


class VehicleEnterprise(BaseModel):
    id: int
    company_name: str
    company_address: str
    contact_email: str

    class Config:
        from_attributes = True


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
    brandmodel: VehicleModelFromDB
    enterprise: VehicleEnterprise | None
