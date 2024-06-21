from typing import Any

import pytz
from sqladmin import ModelView
from starlette.requests import Request

from app.db.models import Vehicle, VehicleBrand, VehicleModel, VehicleTrackPoint


class VehicleAdmin(ModelView, model=Vehicle):
    column_labels = {
        Vehicle.id: "Vehicle id",
        Vehicle.is_in_work: "Vehicle is in work",
        Vehicle.description: "Description",
        Vehicle.created_at: "Created at",
    }
    column_list = [Vehicle.id, Vehicle.is_in_work, Vehicle.description, Vehicle.created_at]
    column_details_list = (
        "id",
        "brandmodel",
        "description",
        "enterprise",
        "drivers",
        "is_in_work",
        "manufactured_year",
        "mileage",
        "cost",
        "purchase_datetime",
        "created_at",
    )
    form_excluded_columns = ("drivers",)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        """Perform some actions before a model is created or updated.
        By default does nothing.
        """
        from main import SERVER_TIME_ZONE

        incomming_purchase_datetime = data.get("purchase_datetime")

        if not incomming_purchase_datetime:
            return None

        default_timezone = pytz.timezone(SERVER_TIME_ZONE)
        data["purchase_datetime"] = incomming_purchase_datetime.replace(tzinfo=default_timezone)


class VehicleBrandAdmin(ModelView, model=VehicleBrand):
    column_labels = {
        VehicleBrand.id: "Brand id",
        VehicleBrand.brand_name: "Brand name",
        VehicleBrand.original_country: "Originaly brand country",
    }
    column_list = [VehicleBrand.id, VehicleBrand.brand_name, VehicleBrand.original_country]


class VehicleModelAdmin(ModelView, model=VehicleModel):
    column_labels = {
        VehicleModel.id: "Model id",
        VehicleModel.exact_model_name: "Model name",
        VehicleModel.brand: "Model brand",
    }
    column_list = [VehicleModel.id, VehicleModel.exact_model_name, VehicleModel.brand]


class VehicleTrackPointAdmin(ModelView, model=VehicleTrackPoint):
    column_labels = {
        VehicleTrackPoint.id: "id",
        VehicleTrackPoint.date_time: "Set date_time",
        "repr_geotag": "Geotag",
        VehicleTrackPoint.vehicle: "Vehicle",
    }
    column_list = [
        VehicleTrackPoint.id,
        VehicleTrackPoint.date_time,
        "repr_geotag",
        VehicleTrackPoint.vehicle,
    ]
