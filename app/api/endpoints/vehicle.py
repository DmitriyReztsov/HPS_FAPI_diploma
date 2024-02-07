from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB, VehiclePartialUpdate
from app.services.vehicle_service import VehicleService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

vehicle_router = APIRouter(prefix="/vehicle", tags=["Vehicle"])


async def get_vehicle_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> VehicleService:
    return VehicleService(uow)


@vehicle_router.get("/vehicles/", response_model=list[VehicleFromDB])
async def get_vehicles(
    vehicle_service: VehicleService = Depends(get_vehicle_service), current_user: str = Depends(get_current_active_user)
):
    allowed_enterprises = [enterprise.id for enterprise in current_user.enterprises]
    filter_set = {"enterprise_id": allowed_enterprises}
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    if current_user.role == "admin":
        return await vehicle_service.get_vehicles()
    elif current_user.role == "manager":
        return await vehicle_service.get_vehicles(filter_set)


@vehicle_router.get("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def retrieve_vehicle(vehicle_id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        return await vehicle_service.retrieve_vehicles(vehicle_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} was not found."
        )


@vehicle_router.post("/vehicles/", response_model=VehicleFromDB, status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle_data: VehicleCreate, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    return await vehicle_service.add_vehicle(vehicle_data)


@vehicle_router.put("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def update_vehicle(
    vehicle_id: int, vehicle_data: VehicleCreate, vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        return await vehicle_service.update_vehicle(vehicle_id, vehicle_data)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} was not found to update."
        )


@vehicle_router.patch("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def partial_update_vehicle(
    vehicle_id: int, vehicle_data: VehiclePartialUpdate, vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        return await vehicle_service.partial_update_vehicle(vehicle_id, vehicle_data)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} was not found to update."
        )


@vehicle_router.delete("/vehicles/{vehicle_id}", response_model=VehicleFromDB)
async def delete_vehicle(vehicle_id: int, vehicle_service: VehicleService = Depends(get_vehicle_service)):
    try:
        return await vehicle_service.delete_vehicle(vehicle_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {vehicle_id} does not exist to delete."
        )
