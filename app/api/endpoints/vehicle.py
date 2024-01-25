from fastapi import APIRouter, Depends, status

from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB
from app.services.vehicle_service import VehicleService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

vehicle_router = APIRouter(prefix="/vehicle", tags=["Vehicle"])


async def get_vehicle_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> VehicleService:
    return VehicleService(uow)


@vehicle_router.get("/vehicles/", response_model=list[VehicleFromDB])
async def get_todos(vehicle_service: VehicleService = Depends(get_vehicle_service)):
    return await vehicle_service.get_vehicles()


@vehicle_router.post("/vehicles/", response_model=VehicleFromDB, status_code=status.HTTP_201_CREATED)
async def create_todo(vehicle_data: VehicleCreate, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    return await vehicle_service.add_vehicle(vehicle_data)
