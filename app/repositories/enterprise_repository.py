from app.db.models import Enterprise
from app.repositories.base_repository import Repository


class EnterpriseRepository(Repository):
    model = Enterprise
