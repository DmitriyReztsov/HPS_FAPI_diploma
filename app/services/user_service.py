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

    # async def get_vehicles(self) -> list[VehicleFromDB]:
    #     async with self.uow:
    #         vehicles: list = await self.uow.vehicle.find_all()
    #         return [VehicleFromDB.model_validate(vehicle) for vehicle in vehicles]

    async def get_user_by_username(self, username: str) -> UserExtended:
        async with self.uow:
            user = await self.uow.user.find_one_by_username(username)
            return UserExtended.model_validate(user)

    async def get_user_by_username_for_login(self, username: str) -> UserLogin:
        async with self.uow:
            user = await self.uow.user.find_one_by_username(username)
            return UserLogin.model_validate(user)

    # async def fake_decode_token(self, token: str) -> UserFromDB:
    #     # This doesn't provide any security at all
    #     # Check the next version
    #     async with self.uow:
    #         user = await self.uow.user.find_one_by_username(token)
    #         return UserFromDB.model_validate(user)

    # async def retrieve_vehicles(self, vehicle_id: int) -> VehicleFromDB:
    #     async with self.uow:
    #         vehicle = await self.uow.vehicle.find_one(vehicle_id)
    #         return VehicleFromDB.model_validate(vehicle)

    # async def update_vehicle(self, vehicle_id: int, vehicle_data: VehicleCreate):
    #     vehicle_dict: dict = vehicle_data.model_dump()
    #     async with self.uow:
    #         vehicle_from_db = await self.uow.vehicle.update_one(vehicle_id, vehicle_dict)
    #         vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

    #         await self.uow.commit()
    #         return vehicle_to_return

    # async def partial_update_vehicle(self, vehicle_id: int, vehicle_data: VehiclePartialUpdate):
    #     vehicle_dict: dict = vehicle_data.model_dump(exclude_unset=True)
    #     async with self.uow:
    #         vehicle_from_db = await self.uow.vehicle.update_one(vehicle_id, vehicle_dict)
    #         vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

    #         await self.uow.commit()
    #         return vehicle_to_return

    # async def delete_vehicle(self, vehicle_id: int):
    #     async with self.uow:
    #         vehicle_from_db = await self.uow.vehicle.delete_one(vehicle_id)
    #         vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

    #         await self.uow.commit()
    #         return vehicle_to_return
