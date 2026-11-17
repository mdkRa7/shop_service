from infrastructure.database.models import Decoration

from .active import ActiveRepository


class DecorationRepository(ActiveRepository[Decoration]):
    model = Decoration
