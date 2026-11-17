from infrastructure.database.models import Filling

from .active import ActiveRepository


class FillingRepository(ActiveRepository[Filling]):
    model = Filling
