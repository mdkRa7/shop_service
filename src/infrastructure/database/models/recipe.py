from decimal import Decimal

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database import Base

from .mixins import CreatedAtMixin, IdPkMixin, UpdatedAtMixin


class Recipe(IdPkMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str] = mapped_column(String(500))
