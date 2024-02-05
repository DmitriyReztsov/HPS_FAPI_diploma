from app.db.models import Driver
from app.repositories.base_repository import Repository


class DriverRepository(Repository):
    model = Driver
