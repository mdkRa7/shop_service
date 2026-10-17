from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import Base

from .mixins import CreatedAtMixin, IdPkMixin, UpdatedAtMixin


class Decoration(IdPkMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )
    price: Mapped[int]
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("true"),
    )
