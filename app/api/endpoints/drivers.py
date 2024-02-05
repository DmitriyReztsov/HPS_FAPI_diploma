from fastapi import APIRouter, Depends

from app.api.schemas.driver import DriverFromDB
from app.services.driver_service import DriverService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

driver_router = APIRouter(prefix="/driver", tags=["Driver"])


async def get_driver_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> DriverService:
    return DriverService(uow)


@driver_router.get("/drivers/", response_model=list[DriverFromDB])
async def get_drivers(driver_service: DriverService = Depends(get_driver_service)):
    return await driver_service.get_drivers()
