from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.driver_repository import DriverRepository
from app.repositories.enterprise_repository import EnterpriseRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.trip_repository import TripRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import (
    VehicleBrandRepository,
    VehicleModelRepository,
    VehicleRepository,
    VehicleTrackPointRepository,
)


class IUnitOfWork(ABC):
    driver: DriverRepository
    enterprise: EnterpriseRepository
    report: ReportRepository
    trip: TripRepository
    user: UserRepository
    vehicle: VehicleRepository
    vehiclebrand: VehicleBrandRepository
    vehiclemodel: VehicleModelRepository
    vehicletrackpoint: VehicleTrackPointRepository

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

        self.driver = DriverRepository(self.session)
        self.enterprise = EnterpriseRepository(self.session)
        self.report = ReportRepository(self.session)
        self.trip = TripRepository(self.session)
        self.user = UserRepository(self.session)
        self.vehicle = VehicleRepository(self.session)
        self.vehiclebrand = VehicleBrandRepository(self.session)
        self.vehiclemodel = VehicleModelRepository(self.session)
        self.vehicletrackpoint = VehicleTrackPointRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
