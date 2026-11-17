import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date
from sqlalchemy import Enum as SAlchemyEnum
from sqlalchemy import ForeignKey, Identity, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from domain.enums import OrderStatus
from infrastructure.database import Base

from .mixins import CreatedAtMixin, IdPkMixin, UpdatedAtMixin


class Order(IdPkMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    user_id: Mapped[uuid.UUID] = mapped_column(index=True)
    number: Mapped[int] = mapped_column(Identity(), unique=True)
    customer_name: Mapped[str] = mapped_column(String(100))
    inscription: Mapped[str | None] = mapped_column(
        String(100),
    )
    phone: Mapped[str] = mapped_column(String(20))
    filling_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fillings.id"))
    decoration_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("decorations.id")
    )
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    pickup_date: Mapped[date] = mapped_column(Date, index=True)
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    status: Mapped[OrderStatus] = mapped_column(
        SAlchemyEnum(OrderStatus, values_callable=lambda x: [e.value for e in x]),
        default=OrderStatus.NEW,
        server_default=OrderStatus.NEW,
    )
