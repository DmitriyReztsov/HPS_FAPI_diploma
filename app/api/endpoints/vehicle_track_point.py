from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.user import UserExtended
from app.api.schemas.vehicle_track_point import (
    VehicleCreateTrackPoint,
    VehicleTrackPoint,
    VehicleTrackPointGeoFromDB,
    VehicleTrackPointGeoJSON,
)
from app.services.vehicle_service import VehicleTrackPointService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

vehicle_track_point_router = APIRouter(prefix="/vehicle_track_point", tags=["VehicleTrackPoint"])


async def get_track_point_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> VehicleTrackPointService:
    return VehicleTrackPointService(uow)


@vehicle_track_point_router.get("/tracks/", response_model=list[VehicleTrackPoint | VehicleTrackPointGeoJSON])
async def get_vehicle_track_points(
    vehicle_track_point_service: VehicleTrackPointService = Depends(get_track_point_service),
    current_user: UserExtended = Depends(get_current_active_user),
    geojson: bool = False,
    vehicle_id: int = None,
    from_date: str = None,
    till_date: str = None,
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await vehicle_track_point_service.get_vehicle_track_points(
        current_user, geojson, vehicle_id, from_date, till_date
    )


@vehicle_track_point_router.get("/tracks/{track_id}", response_model=VehicleTrackPoint | VehicleTrackPointGeoJSON)
async def retrieve_vehicle_track_point(
    track_id: int,
    vehicle_track_point_service: VehicleTrackPointService = Depends(get_track_point_service),
    current_user: UserExtended = Depends(get_current_active_user),
    geojson: bool = False,
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        return await vehicle_track_point_service.retrieve_vehicle_track_point(track_id, current_user, geojson)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle Track Point with id {track_id} was not found."
        )


@vehicle_track_point_router.post(
    "/tracks/", response_model=VehicleTrackPointGeoFromDB, status_code=status.HTTP_201_CREATED
)
async def create_vehicle_track_point(
    vehicle_track_point_data: Annotated[VehicleCreateTrackPoint, Body()],
    vehicle_track_point_service: VehicleTrackPointService = Depends(get_track_point_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        res = await vehicle_track_point_service.add_vehicle_track_point(vehicle_track_point_data, current_user)
        return res
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
