from sqlalchemy import insert, select

from app.db.models import Enterprise, Vehicle, VehicleBrand, VehicleModel
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
