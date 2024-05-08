import math

from fastapi.exceptions import ValidationException

from app.api.schemas.driver import DriverFromDB
from app.api.schemas.user import UserExtended
from app.utils.auth import get_users_enterpises
from app.utils.pagination import PagedResponseSchema, PageParams
from app.utils.unitofwork import IUnitOfWork


class DriverService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_drivers(
        self, current_user: UserExtended = None, page_params: PageParams = None
    ) -> PagedResponseSchema[DriverFromDB]:
        if not current_user:
            return None

        allowed_objects = get_users_enterpises(current_user)
        async with self.uow:
            if current_user.role == "manager" and allowed_objects.get("enterprise_id"):
                drivers: list = await self.uow.driver.find_all_filter_by_enterprise(allowed_objects)
            elif current_user.role == "admin":
                drivers: list = await self.uow.driver.find_all()
            else:
                raise ValidationException({"enterprise_id": "You are not allowed to get drivers for this enterprise"})
            from_index = page_params.page * page_params.size
            to_index = (page_params.page + 1) * page_params.size
            return PagedResponseSchema(
                total=math.ceil(len(drivers) / page_params.size) - 1,
                page=page_params.page,
                size=page_params.size,
                results=[DriverFromDB.model_validate(driver) for driver in drivers[from_index:to_index]],
            )
