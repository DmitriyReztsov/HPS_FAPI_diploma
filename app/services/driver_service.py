from app.api.schemas.driver import DriverFromDB
from app.utils.unitofwork import IUnitOfWork


class DriverService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_drivers(self, filter_set=None) -> list[DriverFromDB]:
        async with self.uow:
            if filter_set.get("enterprise_id"):
                drivers: list = await self.uow.driver.find_all_filter_by_enterprise(filter_set)
            else:
                drivers: list = await self.uow.driver.find_all()
            return [DriverFromDB.model_validate(driver) for driver in drivers]
