from pydantic import BaseModel, ConfigDict


class DriverVehicleFromDB(BaseModel):
    driver_id: int
    vehicle_id: int
    is_active_driver: bool

    class Config:
        from_attributes = True


class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    salary: int
    enterprise_id: int

    class Config:
        from_attributes = True


class DriverFromDB(DriverCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicles: list[DriverVehicleFromDB]
