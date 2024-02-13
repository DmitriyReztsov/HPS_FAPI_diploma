from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.api.schemas.driver import DriverFromDB
from app.api.schemas.vehicle import VehicleFromDB


class UserInEnterprise(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class EnterpriseBase(BaseModel):
    company_name: str
    company_address: str
    contact_email: str

    class Config:
        from_attributes = True


class EnterpriseCreate(EnterpriseBase):
    model_config = ConfigDict(from_attributes=True)

    users: list[int] | None = []


class EnterpriseFromDB(EnterpriseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicles: list[VehicleFromDB]
    drivers: list[DriverFromDB]
    users: Optional[list["UserInEnterprise"]]


class EnterpriseShort(EnterpriseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EnterprisePartialUpdate(BaseModel):
    company_name: str | None = None
    company_address: str | None = None
    contact_email: str | None = None
    users: list[int] | None = []

    class Config:
        from_attributes = True
