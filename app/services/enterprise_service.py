from app.api.schemas.enterprise import EnterpriseFromDB
from app.utils.unitofwork import IUnitOfWork


class EnterpriseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_enterprises(self, filter_set=None) -> list[EnterpriseFromDB]:
        async with self.uow:
            if filter_set.get("enterprise_id"):
                enterprises: list = await self.uow.enterprise.find_all_filter_by_enterprise(filter_set)
            else:
                enterprises: list = await self.uow.enterprise.find_all()
            return [EnterpriseFromDB.model_validate(enterprise) for enterprise in enterprises]
