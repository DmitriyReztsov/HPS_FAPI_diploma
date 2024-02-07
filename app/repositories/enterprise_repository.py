from sqlalchemy import select

from app.db.models import Enterprise
from app.repositories.base_repository import Repository


class EnterpriseRepository(Repository):
    model = Enterprise

    async def find_all_filter_by_enterprise(self, filter_set: dict = None):
        result = await self.session.execute(
            select(self.model).where(self.model.id.in_(filter_set.get("enterprise_id")))
        )
        return result.scalars().all()
