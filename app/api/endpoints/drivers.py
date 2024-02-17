from fastapi import APIRouter, Depends, HTTPException, status

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.driver import DriverFromDB
from app.services.driver_service import DriverService
from app.utils.pagination import PagedResponseSchema, PageParams
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

driver_router = APIRouter(prefix="/driver", tags=["Driver"])


async def get_driver_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> DriverService:
    return DriverService(uow)


@driver_router.get("/drivers/", response_model=PagedResponseSchema[DriverFromDB])
async def get_drivers(
    driver_service: DriverService = Depends(get_driver_service),
    current_user: str = Depends(get_current_active_user),
    page_params: PageParams = Depends(),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await driver_service.get_drivers(current_user, page_params)
