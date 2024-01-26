from fastapi import APIRouter, Depends, status

from app.api.schemas.vehicle_model import VehicleModelCreate, VehicleModelFromDB
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
