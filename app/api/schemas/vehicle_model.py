from pydantic import BaseModel, ConfigDict


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
    exact_model_name: str | None

    model_config = ConfigDict(from_attributes=True)

    id: int
