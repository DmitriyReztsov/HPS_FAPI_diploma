from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB, VehiclePartialUpdate
from app.api.schemas.vehicle_brand import (
    VehicleBrandCreate,
    VehicleBrandFromDB,
    VehicleBrandPartialUpdate,
)
from app.api.schemas.vehicle_model import (
    VehicleModelCreate,
    VehicleModelFromDB,
    VehicleModelPartialUpdate,
)
from app.utils.unitofwork import IUnitOfWork


class VehicleBrandService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_brand(self, vehicle_brand_data: VehicleBrandCreate) -> VehicleBrandFromDB:
        vehicle_brand_dict: dict = vehicle_brand_data.model_dump()
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.add_one(vehicle_brand_dict)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            # если ранее возникнет ошибка при создании объектов, то изменения не сохранятся и откатятся
            await self.uow.commit()
            return vehicle_brand_to_return

    async def get_vehicle_brands(self) -> list[VehicleBrandFromDB]:
        async with self.uow:
            vehicle_brands: list = await self.uow.vehiclebrand.find_all()
            return [VehicleBrandFromDB.model_validate(vehicle_brand) for vehicle_brand in vehicle_brands]

    async def retrieve_vehicle_brands(self, vehicle_brand_id: int) -> VehicleBrandFromDB:
        async with self.uow:
            vehicle_brand = await self.uow.vehiclebrand.find_one(vehicle_brand_id)
            return VehicleBrandFromDB.model_validate(vehicle_brand)

    async def update_vehicle_brand(self, vehicle_brand_id: int, vehicle_brand_data: VehicleBrandCreate):
        vehicle_brand_dict: dict = vehicle_brand_data.model_dump()
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.update_one(vehicle_brand_id, vehicle_brand_dict)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            await self.uow.commit()
            return vehicle_brand_to_return

    async def partial_update_vehicle_brand(self, vehicle_brand_id: int, vehicle_brand_data: VehicleBrandPartialUpdate):
        vehicle_brand_dict: dict = vehicle_brand_data.model_dump(exclude_unset=True)
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.update_one(vehicle_brand_id, vehicle_brand_dict)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            await self.uow.commit()
            return vehicle_brand_to_return

    async def delete_vehicle_brand(self, vehicle_brand_id: int):
        async with self.uow:
            vehicle_brand_from_db = await self.uow.vehiclebrand.delete_one(vehicle_brand_id)
            vehicle_brand_to_return = VehicleBrandFromDB.model_validate(vehicle_brand_from_db)

            await self.uow.commit()
            return vehicle_brand_to_return


class VehicleModelService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_model(self, vehicle_model_data: VehicleModelCreate) -> VehicleModelFromDB:
        vehicle_model_dict: dict = vehicle_model_data.model_dump()
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.add_one(vehicle_model_dict)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            # если ранее возникнет ошибка при создании объектов, то изменения не сохранятся и откатятся
            await self.uow.commit()
            return vehicle_model_to_return

    async def get_vehicle_models(self) -> list[VehicleModelFromDB]:
        async with self.uow:
            vehicle_models: list = await self.uow.vehiclemodel.find_all()
            return [VehicleModelFromDB.model_validate(vehicle_model) for vehicle_model in vehicle_models]

    async def retrieve_vehicle_models(self, vehicle_model_id: int) -> VehicleModelFromDB:
        async with self.uow:
            vehicle_model = await self.uow.vehiclemodel.find_one(vehicle_model_id)
            return VehicleModelFromDB.model_validate(vehicle_model)

    async def update_vehicle_model(self, vehicle_model_id: int, vehicle_model_data: VehicleModelCreate):
        vehicle_model_dict: dict = vehicle_model_data.model_dump()
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.update_one(vehicle_model_id, vehicle_model_dict)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            await self.uow.commit()
            return vehicle_model_to_return

    async def partial_update_vehicle_model(self, vehicle_model_id: int, vehicle_model_data: VehicleModelPartialUpdate):
        vehicle_model_dict: dict = vehicle_model_data.model_dump(exclude_unset=True)
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.update_one(vehicle_model_id, vehicle_model_dict)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            await self.uow.commit()
            return vehicle_model_to_return

    async def delete_vehicle_model(self, vehicle_model_id: int):
        async with self.uow:
            vehicle_model_from_db = await self.uow.vehiclemodel.delete_one(vehicle_model_id)
            vehicle_model_to_return = VehicleModelFromDB.model_validate(vehicle_model_from_db)

            await self.uow.commit()
            return vehicle_model_to_return


class VehicleService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle(self, vehicle_data: VehicleCreate) -> VehicleFromDB:
        vehicle_dict: dict = vehicle_data.model_dump()
        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.add_one(vehicle_dict)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            # если ранее возникнет ошибка при создании объектов, то изменения не сохранятся и откатятся
            await self.uow.commit()
            return vehicle_to_return

    async def get_vehicles(self) -> list[VehicleFromDB]:
        async with self.uow:
            vehicles: list = await self.uow.vehicle.find_all()
            return [VehicleFromDB.model_validate(vehicle) for vehicle in vehicles]

    async def retrieve_vehicles(self, vehicle_id: int) -> VehicleFromDB:
        async with self.uow:
            vehicle = await self.uow.vehicle.find_one(vehicle_id)
            return VehicleFromDB.model_validate(vehicle)

    async def update_vehicle(self, vehicle_id: int, vehicle_data: VehicleCreate):
        vehicle_dict: dict = vehicle_data.model_dump()
        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.update_one(vehicle_id, vehicle_dict)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            await self.uow.commit()
            return vehicle_to_return

    async def partial_update_vehicle(self, vehicle_id: int, vehicle_data: VehiclePartialUpdate):
        vehicle_dict: dict = vehicle_data.model_dump(exclude_unset=True)
        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.update_one(vehicle_id, vehicle_dict)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            await self.uow.commit()
            return vehicle_to_return

    async def delete_vehicle(self, vehicle_id: int):
        async with self.uow:
            vehicle_from_db = await self.uow.vehicle.delete_one(vehicle_id)
            vehicle_to_return = VehicleFromDB.model_validate(vehicle_from_db)

            await self.uow.commit()
            return vehicle_to_return
