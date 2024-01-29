from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.api.schemas.vehicle_brand import (
    VehicleBrandCreate,
    VehicleBrandFromDB,
    VehicleBrandPartialUpdate,
)
from app.services.vehicle_service import VehicleBrandService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

vehicle_brand_router = APIRouter(prefix="/vehicle_brand", tags=["VehicleBrand"])


async def get_vehicle_brand_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> VehicleBrandService:
    return VehicleBrandService(uow)


@vehicle_brand_router.get("/vehicle_brands/", response_model=list[VehicleBrandFromDB])
async def get_vehicle_brands(vehicle_brand_service: VehicleBrandService = Depends(get_vehicle_brand_service)):
    return await vehicle_brand_service.get_vehicle_brands()


@vehicle_brand_router.post("/vehicle_brands/", response_model=VehicleBrandFromDB, status_code=status.HTTP_201_CREATED)
async def create_vehicle_brand(
    vehicle_brand_data: VehicleBrandCreate, vehicle_service: VehicleBrandService = Depends(get_vehicle_brand_service)
):
    return await vehicle_service.add_vehicle_brand(vehicle_brand_data)


@vehicle_brand_router.get("/vehicle_brands/{vehicle_brand_id}", response_model=VehicleBrandFromDB)
async def retrieve_vehicle_brand(
    vehicle_brand_id: int, vehicle_brand_service: VehicleBrandService = Depends(get_vehicle_brand_service)
):
    try:
        return await vehicle_brand_service.retrieve_vehicle_brands(vehicle_brand_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle_model with id {vehicle_brand_id} was not found."
        )


@vehicle_brand_router.put("/vehicle_brands/{vehicle_brand_id}", response_model=VehicleBrandFromDB)
async def update_vehicle_brand(
    vehicle_brand_id: int,
    vehicle_brand_data: VehicleBrandCreate,
    vehicle_brand_service: VehicleBrandService = Depends(get_vehicle_brand_service),
):
    try:
        return await vehicle_brand_service.update_vehicle_brand(vehicle_brand_id, vehicle_brand_data)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle_brand with id {vehicle_brand_id} was not found to update.",
        )


@vehicle_brand_router.patch("/vehicle_brands/{vehicle_brand_id}", response_model=VehicleBrandFromDB)
async def partial_update_vehicle_brand(
    vehicle_brand_id: int,
    vehicle_brand_data: VehicleBrandPartialUpdate,
    vehicle_brand_service: VehicleBrandService = Depends(get_vehicle_brand_service),
):
    try:
        return await vehicle_brand_service.partial_update_vehicle_brand(vehicle_brand_id, vehicle_brand_data)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle_brand with id {vehicle_brand_id} was not found to update.",
        )


@vehicle_brand_router.delete("/vehicle_brands/{vehicle_brand_id}", response_model=VehicleBrandFromDB)
async def delete_vehicle_brand(
    vehicle_brand_id: int, vehicle_brand_service: VehicleBrandService = Depends(get_vehicle_brand_service)
):
    try:
        return await vehicle_brand_service.delete_vehicle_brand(vehicle_brand_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle_brand with id {vehicle_brand_id} does not exist to delete.",
        )
