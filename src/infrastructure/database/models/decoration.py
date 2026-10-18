from sqlalchemy.orm import Mapped

from infrastructure.database import Base

from .mixins import CreatedAtMixin, IdPkMixin, IsActiveMixin, NameMixin, UpdatedAtMixin


class Decoration(
    IdPkMixin, CreatedAtMixin, UpdatedAtMixin, NameMixin, IsActiveMixin, Base
):
    price: Mapped[int]
