from sqlalchemy.orm import Mapped

from infrastructure.database import Base

from .mixins import CreatedAtMixin, IdPkMixin, IsActiveMixin, NameMixin, UpdatedAtMixin


class Filling(
    IdPkMixin, CreatedAtMixin, UpdatedAtMixin, NameMixin, IsActiveMixin, Base
):
    price_per_kg: Mapped[int]
