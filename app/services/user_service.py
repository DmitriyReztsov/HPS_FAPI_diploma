from app.api.schemas.user import UserCreate, UserExtended, UserFromDB, UserLogin
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user_data: UserCreate) -> UserFromDB:
        user_dict: dict = user_data.model_dump()
        async with self.uow:
            user_from_db = await self.uow.user.add_one(user_dict)
            user_to_return = UserFromDB.model_validate(user_from_db)

            await self.uow.commit()
            return user_to_return

    async def get_user_by_username(self, username: str) -> UserExtended:
        async with self.uow:
            user = await self.uow.user.find_one_by_username(username)
            return UserExtended.model_validate(user)

    async def get_user_by_username_for_login(self, username: str) -> UserLogin:
        async with self.uow:
            user = await self.uow.user.find_one_by_username(username)
            return UserLogin.model_validate(user)
