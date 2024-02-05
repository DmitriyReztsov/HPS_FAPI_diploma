from fastapi import APIRouter, Depends

from app.api.schemas.enterprise import EnterpriseFromDB
from app.services.enterprise_service import EnterpriseService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

enterprise_router = APIRouter(prefix="/enterprise", tags=["Enterprise"])


async def get_enterprise_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> EnterpriseService:
    return EnterpriseService(uow)


@enterprise_router.get("/enterprises/", response_model=list[EnterpriseFromDB])
async def get_enterprises(enterprise_service: EnterpriseService = Depends(get_enterprise_service)):
    return await enterprise_service.get_enterprises()
