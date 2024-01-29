from pydantic import BaseModel, ConfigDict


class VehicleBrandCreate(BaseModel):
    brand_name: str
    original_country: str


class VehicleBrandPartialUpdate(BaseModel):
    brand_name: str | None = None
    original_country: str | None = None


class VehicleBrandFromDB(VehicleBrandCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
