from fastapi import APIRouter, Depends, HTTPException, status

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.enterprise import EnterpriseFromDB
from app.services.enterprise_service import EnterpriseService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

enterprise_router = APIRouter(prefix="/enterprise", tags=["Enterprise"])


async def get_enterprise_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> EnterpriseService:
    return EnterpriseService(uow)


@enterprise_router.get("/enterprises/", response_model=list[EnterpriseFromDB])
async def get_enterprises(
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: str = Depends(get_current_active_user),
):
    allowed_enterprises = [enterprise.id for enterprise in current_user.enterprises]
    filter_set = {"enterprise_id": allowed_enterprises}
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    if current_user.role == "admin":
        return await enterprise_service.get_enterprises()
    elif current_user.role == "manager":
        return await enterprise_service.get_enterprises(filter_set)
