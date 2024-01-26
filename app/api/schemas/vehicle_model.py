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


class VehicleModelFromDB(VehicleModelCreate):
    exact_model_name: str | None

    model_config = ConfigDict(from_attributes=True)

    id: int
