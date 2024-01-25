from app.db.models import Vehicle
from app.repositories.base_repository import Repository


class VehicleRepository(Repository):
    model = Vehicle
