from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.user import UserExtended
from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB, VehiclePartialUpdate, VehicleNamesFromDB
from app.services.vehicle_service import VehicleService
from app.utils.pagination import PagedResponseSchema, PageParams
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

vehicle_router = APIRouter(prefix="/vehicle", tags=["Vehicle"])


async def get_vehicle_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> VehicleService:
    return VehicleService(uow)


@vehicle_router.get("/vehicles/", response_model=PagedResponseSchema[VehicleFromDB])
async def get_vehicles(
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: UserExtended = Depends(get_current_active_user),
    page_params: PageParams = Depends(),
    enterprise_id: int = None,
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await vehicle_service.get_vehicles(current_user, page_params, enterprise_id)


@vehicle_router.get("/vehicles_names/", response_model=list[VehicleNamesFromDB])
async def get_vehicles_names(
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    enterprise_id: int = None,
):
    return await vehicle_service.get_vehicles_names(enterprise_id)


@vehicle_router.get("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def retrieve_vehicle(
    vehicle_id: int,
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        return await vehicle_service.retrieve_vehicles(vehicle_id, current_user)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} was not found."
        )


@vehicle_router.post("/vehicles/", response_model=VehicleFromDB, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: Annotated[VehicleCreate, Body()],
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        return await vehicle_service.add_vehicle(vehicle_data, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())


@vehicle_router.put("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: Annotated[VehicleCreate, Body()],
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    try:
        return await vehicle_service.update_vehicle(vehicle_id, vehicle_data, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} was not found to update."
        )


@vehicle_router.patch("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def partial_update_vehicle(
    vehicle_id: int,
    vehicle_data: Annotated[VehiclePartialUpdate, Body()],
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    try:
        return await vehicle_service.partial_update_vehicle(vehicle_id, vehicle_data, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} was not found to update."
        )


@vehicle_router.delete("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def delete_vehicle(
    vehicle_id: int,
    vehicle_service: VehicleService = Depends(get_vehicle_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    try:
        return await vehicle_service.delete_vehicle(vehicle_id, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} does not exist to delete."
        )
