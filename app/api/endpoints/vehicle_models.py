from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.api.schemas.vehicle_model import (
    VehicleModelCreate,
    VehicleModelFromDB,
    VehicleModelPartialUpdate,
)
from app.services.vehicle_service import VehicleModelService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

vehicle_model_router = APIRouter(prefix="/vehicle_model", tags=["VehicleModel"])


async def get_vehicle_model_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> VehicleModelService:
    return VehicleModelService(uow)


@vehicle_model_router.get("/vehicle_models/", response_model=list[VehicleModelFromDB])
async def get_vehicle_models(vehicle_model_service: VehicleModelService = Depends(get_vehicle_model_service)):
    return await vehicle_model_service.get_vehicle_models()


@vehicle_model_router.post("/vehicle_models/", response_model=VehicleModelFromDB, status_code=status.HTTP_201_CREATED)
async def create_vehicle_model(
    vehicle_model_data: VehicleModelCreate,
    vehicle_model_service: VehicleModelService = Depends(get_vehicle_model_service),
):
    return await vehicle_model_service.add_vehicle_model(vehicle_model_data)


@vehicle_model_router.get("/vehicle_models/{vehicle_model_id}", response_model=VehicleModelFromDB)
async def retrieve_vehicle_model(
    vehicle_model_id: int, vehicle_model_service: VehicleModelService = Depends(get_vehicle_model_service)
):
    try:
        return await vehicle_model_service.retrieve_vehicle_models(vehicle_model_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle_model with id {vehicle_model_id} was not found."
        )


@vehicle_model_router.put("/vehicle_models/{vehicle_model_id}", response_model=VehicleModelFromDB)
async def update_vehicle_model(
    vehicle_model_id: int,
    vehicle_model_data: VehicleModelCreate,
    vehicle_model_service: VehicleModelService = Depends(get_vehicle_model_service),
):
    try:
        return await vehicle_model_service.update_vehicle_model(vehicle_model_id, vehicle_model_data)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle_model with id {vehicle_model_id} was not found to update.",
        )


@vehicle_model_router.patch("/vehicle_models/{vehicle_model_id}", response_model=VehicleModelFromDB)
async def partial_update_vehicle_model(
    vehicle_model_id: int,
    vehicle_model_data: VehicleModelPartialUpdate,
    vehicle_model_service: VehicleModelService = Depends(get_vehicle_model_service),
):
    try:
        return await vehicle_model_service.partial_update_vehicle_model(vehicle_model_id, vehicle_model_data)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle_model with id {vehicle_model_id} was not found to update.",
        )


@vehicle_model_router.delete("/vehicle_models/{vehicle_model_id}", response_model=VehicleModelFromDB)
async def delete_vehicle_model(
    vehicle_model_id: int, vehicle_model_service: VehicleModelService = Depends(get_vehicle_model_service)
):
    try:
        return await vehicle_model_service.delete_vehicle_model(vehicle_model_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle_model with id {vehicle_model_id} does not exist to delete.",
        )
