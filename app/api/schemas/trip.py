from datetime import datetime

from geopy.geocoders import Nominatim
from pydantic import BaseModel, ConfigDict


class TripPointsForMap(BaseModel):
    trip_ids: list


class TripCreate(BaseModel):
    start_date_time: datetime
    finish_date_time: datetime
    vehicle_id: int

    class Config:
        from_attributes = True


class TripFromDB(TripCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TripFromDBWithExtraData(BaseModel):
    id: int
    start_date_time: datetime
    finish_date_time: datetime
    start_point_geo: tuple[float, float]
    finish_point_geo: tuple[float, float]
    start_address: str
    finish_address: str

    class Config:
        from_attributes = True


def get_address_by_point(point_coords: tuple):
    geolocator = Nominatim(user_agent="FAPI_HPS")
    location = geolocator.reverse(f"{point_coords[0]}, {point_coords[1]}")
    return location.address
