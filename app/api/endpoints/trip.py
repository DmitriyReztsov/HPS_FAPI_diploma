from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.trip import (
    TripCreate,
    TripFromDB,
    TripFromDBWithExtraData,
    TripPointsForMap,
)
from app.api.schemas.user import UserExtended
from app.api.schemas.vehicle_track_point import (
    VehicleTrackPoint,
    VehicleTrackPointGeoJSON,
)
from app.services.trip_service import TripService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

trip_router = APIRouter(prefix="/trip", tags=["Trip"])


async def get_trip_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TripService:
    return TripService(uow)


@trip_router.get("/trips/", response_model=list[TripFromDB])
async def get_trips(
    trip_service: TripService = Depends(get_trip_service),
    current_user: UserExtended = Depends(get_current_active_user),
    geojson: bool = False,
    vehicle_id: int = None,
    from_date: str = None,
    till_date: str = None,
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await trip_service.get_trips(current_user, geojson, vehicle_id, from_date, till_date)


@trip_router.get("/trips/with_track_by_vehicle/", response_model=list[VehicleTrackPoint | VehicleTrackPointGeoJSON])
async def get_trips_with_track_by_vehicle(
    trip_service: TripService = Depends(get_trip_service),
    current_user: UserExtended = Depends(get_current_active_user),
    vehicle_id: int = None,
    from_date: datetime = None,
    till_date: datetime = None,
    geojson: bool = False,
) -> list[VehicleTrackPoint | VehicleTrackPointGeoJSON]:
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await trip_service.get_trips_points_by_vehicle(current_user, vehicle_id, from_date, till_date, geojson)


@trip_router.get("/trips/by_vehicle/", response_model=list[TripFromDBWithExtraData])
async def get_trips_by_vehicle(
    trip_service: TripService = Depends(get_trip_service),
    current_user: UserExtended = Depends(get_current_active_user),
    vehicle_id: int = None,
    from_date: datetime = None,
    till_date: datetime = None,
    geojson: bool = False,
) -> list[TripFromDBWithExtraData]:
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await trip_service.get_trips_by_vehicle(current_user, vehicle_id, from_date, till_date, geojson)


@trip_router.post("/get_map_for_trip/{vehicle_id}", status_code=status.HTTP_200_OK)
async def create_map_for_trip(
    trip_ids: Annotated[TripPointsForMap, Body()],
    trip_service: TripService = Depends(get_trip_service),
    vehicle_id: int = None,
):
    await trip_service.create_map(vehicle_id, trip_ids)


@trip_router.get("/trips/{trip_id}", response_model=TripFromDB)
async def retrieve_trip(
    trip_service: TripService = Depends(get_trip_service),
    current_user: UserExtended = Depends(get_current_active_user),
    geojson: bool = False,
    trip_id: int = None,
    from_date: str = None,
    till_date: str = None,
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        return await trip_service.retrieve_trip(trip_id, from_date, till_date, current_user, geojson)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trip with id {trip_id} was not found.")


@trip_router.post("/trips/", response_model=TripFromDB, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip_data: Annotated[TripCreate, Body()],
    trip_service: TripService = Depends(get_trip_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        res = await trip_service.add_trip(trip_data, current_user)
        return res
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
