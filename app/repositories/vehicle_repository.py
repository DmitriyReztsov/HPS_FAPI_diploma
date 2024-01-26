from app.db.models import Vehicle, VehicleBrand, VehicleModel
from app.repositories.base_repository import Repository


class VehicleBrandRepository(Repository):
    model = VehicleBrand


class VehicleModelRepository(Repository):
    model = VehicleModel


class VehicleRepository(Repository):
    model = Vehicle
