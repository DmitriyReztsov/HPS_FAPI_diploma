from pydantic import BaseModel, ConfigDict

from app.api.schemas.vehicle_brand import VehicleBrandFromDB


class VehicleModelCreate(BaseModel):
    brand_id: int  # id of brand name
    exact_model_name: str
    vehicle_type: str
    passenger_capacity: int
    tonnage: int
    fuel_capacity: int

    class Config:
        from_attributes = True


class VehicleModelPartialUpdate(BaseModel):
    brand_id: int | None = None
    exact_model_name: str | None = None
    vehicle_type: str | None = None
    passenger_capacity: int | None = None
    tonnage: int | None = None
    fuel_capacity: int | None = None


class VehicleModelFromDB(VehicleModelCreate):
    id: int
    exact_model_name: str | None
    brand: VehicleBrandFromDB

    model_config = ConfigDict(from_attributes=True)


class VehicleBrandModel(BaseModel):
    id: int
    brand_name: str
    exact_model_name: str
