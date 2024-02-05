from typing import Any

from sqladmin import ModelView
from sqlalchemy import or_, update
from starlette.requests import Request

from app.db.database import async_session_maker
from app.db.models import Driver, DriverVehicle


class DriverAdmin(ModelView, model=Driver):
    column_labels = {Driver.id: "Driver id", Driver.get_full_name: "Full name"}
    column_list = [Driver.id, Driver.get_full_name]
    column_details_list = ("id", "first_name", "last_name", "enterprise", "salary", "vehicles")
    form_excluded_columns = ("vehicles",)  # assignation of driver on vehicle should be processed in Drive Vehicle model


class DriverVehicleAdmin(ModelView, model=DriverVehicle):
    column_list = [DriverVehicle.driver, DriverVehicle.vehicle, DriverVehicle.is_active_driver]

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        """Perform some actions before a model is created or updated.
        By default does nothing.
        """
        is_active_driver = data.get("is_active_driver")

        if not is_active_driver:
            return None

        driver_id = int(data.get("driver"))
        vehicle_id = int(data.get("vehicle"))
        stmt = (
            update(DriverVehicle)
            .where(or_(DriverVehicle.driver_id == driver_id, DriverVehicle.vehicle_id == vehicle_id))
            .values(is_active_driver=False)
        )

        session = async_session_maker()
        await session.execute(stmt)
        await session.commit()
        await session.close()
