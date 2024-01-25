from app.api.schemas.vehicle import VehicleCreate, VehicleFromDB
from app.utils.unitofwork import IUnitOfWork


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
