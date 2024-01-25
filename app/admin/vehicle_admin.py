from sqladmin import ModelView

from app.db.models import Vehicle


class VehicleAdmin(ModelView, model=Vehicle):
    column_list = [Vehicle.id, Vehicle.is_in_work, Vehicle.description, Vehicle.created_at]
