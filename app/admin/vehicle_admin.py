from sqladmin import ModelView

from app.db.models import Vehicle, VehicleBrand, VehicleModel


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
        "created_at",
    )
    form_excluded_columns = ("drivers",)


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
