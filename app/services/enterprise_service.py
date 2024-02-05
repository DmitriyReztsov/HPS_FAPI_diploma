from app.api.schemas.enterprise import EnterpriseFromDB
from app.utils.unitofwork import IUnitOfWork


class EnterpriseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_enterprises(self) -> list[EnterpriseFromDB]:
        async with self.uow:
            enterprises: list = await self.uow.enterprise.find_all()
            return [EnterpriseFromDB.model_validate(enterprise) for enterprise in enterprises]
