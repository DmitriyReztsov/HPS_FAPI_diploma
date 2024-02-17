from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def find_all(self):
        stmt = select(self.model).order_by(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_filter_by_enterprise(self, filter_set: dict = None):
        stmt = (
            select(self.model)
            .where(self.model.enterprise_id.in_(filter_set.get("enterprise_id")))
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_filter_by_id(self, ids: list = None):
        result = await self.session.execute(select(self.model).where(self.model.id.in_(ids)))
        return result.scalars().all()

    async def find_one(self, item_id: int):
        result = await self.session.execute(select(self.model).where(self.model.id == item_id))
        return result.scalar_one()

    async def update_one(self, item_id: int, data: dict):
        query = update(self.model).where(self.model.id == item_id).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete_one(self, item_id: int):
        query = delete(self.model).where(self.model.id == item_id).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()
