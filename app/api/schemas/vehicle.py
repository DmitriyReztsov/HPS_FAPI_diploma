from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.api.schemas.schema_mixin import SchemaMixin
from app.api.schemas.vehicle_model import VehicleModelFromDB


class VehicleEnterprise(BaseModel):
    id: int
    company_name: str
    company_address: str
    contact_email: str
    company_timezone: str

    class Config:
        from_attributes = True


class VehicleCreate(BaseModel, SchemaMixin):
    brandmodel_id: int
    description: str
    cost: int
    manufactured_year: int
    mileage: int
    purchase_datetime: datetime
    is_in_work: bool | None = True
    enterprise_id: int | None = None

    class Config:
        from_attributes = True


class VehiclePartialUpdate(BaseModel, SchemaMixin):
    brandmodel_id: int | None = None
    description: str | None = None
    cost: int | None = None
    manufactured_year: int | None = None
    mileage: int | None = None
    purchase_datetime: datetime | None
    is_in_work: bool | None = None
    enterprise_id: int | None = None


class VehicleFromDB(VehicleCreate, SchemaMixin):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    brandmodel: VehicleModelFromDB
    purchase_datetime: datetime | None
    enterprise: VehicleEnterprise | None

    @classmethod
    def model_validate_datetime_with_tz(cls, obj, tz="UTC"):
        obj = cls.set_user_timezone_to_datetime_fields(obj, tz)

        return cls.model_validate(obj)
