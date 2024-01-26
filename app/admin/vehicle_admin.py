from sqladmin import ModelView

from app.db.models import Vehicle, VehicleBrand, VehicleModel


class VehicleAdmin(ModelView, model=Vehicle):
    column_list = [Vehicle.id, Vehicle.is_in_work, Vehicle.description, Vehicle.created_at]


class VehicleBrandAdmin(ModelView, model=VehicleBrand):
    column_list = [VehicleBrand.id, VehicleBrand.brand_name, VehicleBrand.original_country]


class VehicleModelAdmin(ModelView, model=VehicleModel):
    column_list = [VehicleModel.id, VehicleModel.exact_model_name, VehicleModel.brand]
