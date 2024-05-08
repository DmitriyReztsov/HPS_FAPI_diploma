from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ValidationException
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.user import get_current_active_user
from app.api.schemas.enterprise import (
    EnterpriseCreate,
    EnterpriseFromDB,
    EnterprisePartialUpdate,
    EnterpriseShort,
)
from app.api.schemas.user import UserExtended
from app.services.enterprise_service import EnterpriseService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

enterprise_router = APIRouter(prefix="/enterprise", tags=["Enterprise"])


async def get_enterprise_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> EnterpriseService:
    return EnterpriseService(uow)


@enterprise_router.get("/enterprises/short/", response_model=list[EnterpriseShort])
async def get_enterprises_short(
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: str = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await enterprise_service.get_enterprises_short(current_user)


@enterprise_router.get("/enterprises/", response_model=list[EnterpriseFromDB])
async def get_enterprises(
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: str = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    return await enterprise_service.get_enterprises(current_user)


@enterprise_router.get("/enterprises/{enterprise_id}", response_model=EnterpriseFromDB)
async def retrieve_enterprise(
    enterprise_id: int,
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        return await enterprise_service.retrieve_enterprises(enterprise_id, current_user)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Enterprise with id {enterprise_id} was not found."
        )
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())


@enterprise_router.post("/enterprises/", response_model=EnterpriseFromDB, status_code=status.HTTP_201_CREATED)
async def create_enterprise(
    enterprise_data: EnterpriseCreate,
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    if current_user.role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You should have a role in a compmany.")
    try:
        return await enterprise_service.add_enterprise(enterprise_data, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())


@enterprise_router.put("/enterprises/{enterprise_id}", response_model=EnterpriseFromDB)
async def update_enterprise(
    enterprise_id: int,
    enterprise_data: EnterpriseCreate,
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    try:
        return await enterprise_service.update_enterprise(enterprise_id, enterprise_data, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Enterprise with id {enterprise_id} was not found to update."
        )


@enterprise_router.patch("/enterprises/{enterprise_id}", response_model=EnterpriseFromDB)
async def partial_update_enterprise(
    enterprise_id: int,
    enterprise_data: EnterprisePartialUpdate,
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    try:
        return await enterprise_service.partial_update_enterprise(enterprise_id, enterprise_data, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Enterprise with id {enterprise_id} was not found to update."
        )


@enterprise_router.delete("/enterprises/{enterprise_id}", response_model=EnterpriseFromDB)
async def delete_enterprise(
    enterprise_id: int,
    enterprise_service: EnterpriseService = Depends(get_enterprise_service),
    current_user: UserExtended = Depends(get_current_active_user),
):
    try:
        return await enterprise_service.delete_enterprise(enterprise_id, current_user)
    except ValidationException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.errors())
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enterprise with id {enterprise_id} does not exist to delete.",
        )
