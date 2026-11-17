import uuid
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from domain.enums import OrderStatus


@dataclass(frozen=True, slots=True)
class BaseOrderDTO:
    user_id: uuid.UUID
    filling_id: uuid.UUID
    decoration_id: uuid.UUID | None
    weight_kg: Decimal
    phone: str
    customer_name: str
    inscription: str | None
    pickup_date: date


@dataclass(frozen=True, slots=True)
class OutputOrderDTO(BaseOrderDTO):
    id: uuid.UUID
    number: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CreateOrderDTO(BaseOrderDTO):
    expected_price: Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderListItemDTO:
    id: uuid.UUID
    number: int
    customer_name: str
    filling_name: str
    pickup_date: date
    status: OrderStatus


@dataclass(frozen=True, slots=True)
class OrderListDTO:
    total: int
    items: list[OutputOrderDTO]


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderDetailDTO:
    id: uuid.UUID
    number: int
    customer_name: str
    phone: str
    filling_name: str
    decoration_name: str | None
    weight_kg: Decimal
    inscription: str | None
    total_price: Decimal
    pickup_date: date
    status: OrderStatus
    created_at: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class OrderStatusDTO:
    id: uuid.UUID
    status: OrderStatus
