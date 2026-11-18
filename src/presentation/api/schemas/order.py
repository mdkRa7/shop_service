import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from domain.enums import OrderStatus

WeightDecimal = Annotated[Decimal, Field(ge=1, le=10, max_digits=4, decimal_places=2)]


class CakeSelection(BaseModel):
    recipe_id: uuid.UUID | None = None
    filling_id: uuid.UUID | None = None
    decoration_id: uuid.UUID | None = None

    @model_validator(mode="after")
    def check_kind(self):
        if self.recipe_id is not None:
            if self.filling_id is not None or self.decoration_id is not None:
                raise ValueError("recipe_id нельзя сочетать с filling_id/decoration_id")
        elif self.filling_id is None:
            raise ValueError("нужен recipe_id или filling_id")
        return self


class OrderBase(CakeSelection):
    customer_name: str = Field(max_length=100)
    phone: str = Field(max_length=20)
    pickup_date: date
    weight_kg: WeightDecimal
    inscription: str | None = Field(default=None, max_length=100)


class PriceCalculateRequest(CakeSelection):
    weight_kg: WeightDecimal


# class OrderBase(BaseModel):
#     customer_name: str = Field(max_length=100)
#     phone: str = Field(max_length=20)
#     pickup_date: date
#     weight_kg: WeightDecimal
#     recipe_id: uuid.UUID | None = None
#     filling_id: uuid.UUID | None = None
#     decoration_id: uuid.UUID | None = None
#     inscription: str | None = Field(default=None, max_length=100)
#
#     @model_validator(mode="after")
#     def check_kind(self):
#         if self.recipe_id is not None:
#             if self.filling_id is not None or self.decoration_id is not None:
#                 raise ValueError("recipe_id нельзя сочетать с filling_id/decoration_id")
#         elif self.filling_id is None:
#             raise ValueError("нужен recipe_id или filling_id")
#
#         return self


class OrderRead(OrderBase):
    id: uuid.UUID
    number: int
    status: OrderStatus
    total_price: Decimal
    created_at: datetime


class OrderAdd(OrderBase):
    expected_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


# class PriceCalculateRequest(BaseModel):
#     weight_kg: WeightDecimal
#     filling_id: uuid.UUID
#     decoration_id: uuid.UUID | None = None


class PriceRead(BaseModel):
    total_price: Decimal


class OrderListItemRead(BaseModel):
    id: uuid.UUID
    number: int
    customer_name: str
    recipe_name: str | None
    filling_name: str | None
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
    filling_name: str | None
    recipe_name: str | None
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
