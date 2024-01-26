from fastapi import APIRouter, Depends, status

from app.api.schemas.vehicle_brand import VehicleBrandCreate, VehicleBrandFromDB
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
