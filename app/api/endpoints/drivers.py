from fastapi import APIRouter, Depends, HTTPException, status

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.driver import DriverFromDB
from app.services.driver_service import DriverService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

driver_router = APIRouter(prefix="/driver", tags=["Driver"])


async def get_driver_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> DriverService:
    return DriverService(uow)


@driver_router.get("/drivers/", response_model=list[DriverFromDB])
async def get_drivers(
    driver_service: DriverService = Depends(get_driver_service), current_user: str = Depends(get_current_active_user)
):
    allowed_enterprises = [enterprise.id for enterprise in current_user.enterprises]
    filter_set = {"enterprise_id": allowed_enterprises}
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    if current_user.role == "admin":
        return await driver_service.get_drivers()
    elif current_user.role == "manager":
        return await driver_service.get_drivers(filter_set)
