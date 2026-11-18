import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class UnconfirmedOrderRead(BaseModel):
    id: uuid.UUID
    number: int
    customer_name: str
    recipe_name: str | None
    filling_name: str | None
    pickup_date: date


class DashboardSummaryRead(BaseModel):
    day: date
    new_orders_count: int
    revenue: Decimal
    unconfirmed_count: int
    unconfirmed: list[UnconfirmedOrderRead]
