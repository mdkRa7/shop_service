import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

from domain.enums import OrderStatus

WeightDecimal = Annotated[Decimal, Field(ge=1, le=10, max_digits=4, decimal_places=2)]


class OrderBase(BaseModel):
    customer_name: str = Field(max_length=100)
    phone: str = Field(max_length=20)
    pickup_date: date
    weight_kg: WeightDecimal
    filling_id: uuid.UUID
    decoration_id: uuid.UUID | None = None
    inscription: str | None = Field(default=None, max_length=100)


class OrderRead(OrderBase):
    id: uuid.UUID
    number: int
    status: OrderStatus
    total_price: Decimal
    created_at: datetime


class OrderAdd(OrderBase):
    expected_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class PriceCalculateRequest(BaseModel):
    weight_kg: WeightDecimal
    filling_id: uuid.UUID
    decoration_id: uuid.UUID | None = None


class PriceRead(BaseModel):
    total_price: Decimal


class OrderListItemRead(BaseModel):
    id: uuid.UUID
    number: int
    customer_name: str
    filling_name: str
    pickup_date: date
    status: OrderStatus


class OrderListRead(BaseModel):
    total: int
    items: list[OrderListItemRead]


class OrderDetailRead(BaseModel):
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


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderStatusRead(BaseModel):
    id: uuid.UUID
    status: OrderStatus
