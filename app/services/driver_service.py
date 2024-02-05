from app.api.schemas.driver import DriverFromDB
from app.utils.unitofwork import IUnitOfWork


class DriverService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_drivers(self) -> list[DriverFromDB]:
        async with self.uow:
            drivers: list = await self.uow.driver.find_all()
            return [DriverFromDB.model_validate(driver) for driver in drivers]
