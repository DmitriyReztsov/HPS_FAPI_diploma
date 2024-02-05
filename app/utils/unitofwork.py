from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.driver_repository import DriverRepository
from app.repositories.enterprise_repository import EnterpriseRepository
from app.repositories.vehicle_repository import (
    VehicleBrandRepository,
    VehicleModelRepository,
    VehicleRepository,
)


class IUnitOfWork(ABC):
    vehicle: VehicleRepository
    vehiclebrand: VehicleBrandRepository
    vehiclemodel: VehicleModelRepository
    driver: DriverRepository
    enterprise: EnterpriseRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.vehicle = VehicleRepository(self.session)
        self.vehiclebrand = VehicleBrandRepository(self.session)
        self.vehiclemodel = VehicleModelRepository(self.session)
        self.driver = DriverRepository(self.session)
        self.enterprise = EnterpriseRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
