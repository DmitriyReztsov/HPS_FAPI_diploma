from sqlalchemy import and_, insert, select

from app.db.models import (
    Enterprise,
    Vehicle,
    VehicleBrand,
    VehicleModel,
    VehicleTrackPoint,
)
from app.repositories.base_repository import Repository


class VehicleBrandRepository(Repository):
    model = VehicleBrand


class VehicleModelRepository(Repository):
    model = VehicleModel

    async def find_all_brandmodels(self):
        stmt = select(self.model).join(VehicleBrand, VehicleModel.brand_id == VehicleBrand.id).order_by(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class VehicleRepository(Repository):
    model = Vehicle

    async def find_all_with_brandmodel(self):
        stmt = (
            select(self.model)
            .join(VehicleModel, Vehicle.brandmodel_id == VehicleModel.id)
            .join(VehicleBrand, VehicleModel.brand_id == VehicleBrand.id)
            .join(Enterprise, Vehicle.enterprise_id == Enterprise.id, isouter=True)
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all_with_brandmodel_filter_by_enterprise(self, filter_set: dict = None):
        stmt = (
            select(self.model)
            .join(VehicleModel, Vehicle.brandmodel_id == VehicleModel.id)
            .join(VehicleBrand, VehicleModel.brand_id == VehicleBrand.id)
            .join(Enterprise, Vehicle.enterprise_id == Enterprise.id, isouter=True)
            .where(self.model.enterprise_id.in_(filter_set.get("enterprise_id")))
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def find_one(self, item_id: int):
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == item_id)
            .join(VehicleModel, Vehicle.brandmodel_id == VehicleModel.id)
            .join(VehicleBrand, VehicleModel.brand_id == VehicleBrand.id)
            .join(Enterprise, Vehicle.enterprise_id == Enterprise.id, isouter=True)
        )
        return result.scalar_one()


class VehicleTrackPointRepository(Repository):
    model = VehicleTrackPoint

    async def find_all_filter_by_enterprise(self, filter_set: dict = None):
        stmt = (
            select(self.model)
            .join(Vehicle, self.model.vehicle_id == Vehicle.id)
            .where(Vehicle.enterprise_id.in_(filter_set.get("enterprise_id")))
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_one_by_eneterprise(self, item_id: int, filter_set: dict = None):
        stmt = (
            select(self.model)
            .join(Vehicle, self.model.vehicle_id == Vehicle.id)
            .where(Vehicle.enterprise_id.in_(filter_set.get("enterprise_id")))
            .where(self.model.id == item_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def find_all_with_filters(self, filter_set: dict, allowed_objects: dict = None):
        filters_list = []
        if allowed_objects is not None:
            filters_list.append(Vehicle.enterprise_id.in_(allowed_objects.get("enterprise_id")))
        for filter_name, filter_value in filter_set.items():
            match filter_name, filter_value:
                case "vehicle_id", value if value is not None:
                    filters_list.append(self.model.vehicle_id == filter_value)
        stmt = (
            select(self.model)
            .join(Vehicle, self.model.vehicle_id == Vehicle.id)
            .where(and_(*filters_list))
            .where(Vehicle.enterprise_id.in_(allowed_objects.get("enterprise_id")))
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
