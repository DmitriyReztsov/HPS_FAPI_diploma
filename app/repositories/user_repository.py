from sqlalchemy import select

from app.db.models import User
from app.repositories.base_repository import Repository


class UserRepository(Repository):
    model = User

    async def find_one_by_username(self, username: str):
        result = await self.session.execute(select(self.model).where(self.model.username == username))
        return result.scalar_one()
