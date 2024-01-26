from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB
from app.api.schemas.vehicle_brand import VehicleBrandCreate, VehicleBrandFromDB
from app.api.schemas.vehicle_model import VehicleModelCreate, VehicleModelFromDB
from app.utils.unitofwork import IUnitOfWork


class VehicleBrandService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_brand(self, vehicle_brand: VehicleBrandCreate) -> VehicleBrandFromDB:
        vehicle_brand_dict: dict = vehicle_brand.model_dump()
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


class VehicleModelService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle_model(self, vehicle_model: VehicleModelCreate) -> VehicleModelFromDB:
        vehicle_model_dict: dict = vehicle_model.model_dump()
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


class VehicleService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_vehicle(self, vehicle: VehicleCreate) -> VehicleFromDB:
        vehicle_dict: dict = vehicle.model_dump()
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
