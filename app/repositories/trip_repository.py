from sqlalchemy import and_, select

from app.db.models import Trip, Vehicle
from app.repositories.base_repository import Repository


class TripRepository(Repository):
    model = Trip

    async def find_all_with_filters(self, filter_set: dict, allowed_objects: dict = None):
        filters_list = []
        if allowed_objects is not None:
            filters_list.append(Vehicle.enterprise_id.in_(allowed_objects.get("enterprise_id")))
        for filter_name, filter_value in filter_set.items():
            match filter_name, filter_value:
                case "vehicle_id", value if value is not None:
                    filters_list.append(self.model.vehicle_id == filter_value)
                case "from_date", value if value is not None:
                    filters_list.append(self.model.start_date_time >= filter_value)
                case "till_date", value if value is not None:
                    filters_list.append(self.model.finish_date_time <= filter_value)
                case "trip_ids", value if value is not None and isinstance(value, list):
                    filters_list.append(self.model.id.in_(value))
        stmt = (
            select(self.model)
            .join(Vehicle, self.model.vehicle_id == Vehicle.id)
            .where(and_(*filters_list))
            .order_by(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
