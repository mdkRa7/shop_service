import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class UnconfirmedOrderDTO:
    id: uuid.UUID
    number: int
    customer_name: str
    recipe_name: str | None
    filling_name: str | None
    pickup_date: date


@dataclass(frozen=True, slots=True, kw_only=True)
class DashboardSummaryDTO:
    day: date
    new_orders_count: int
    revenue: Decimal
    unconfirmed_count: int
    unconfirmed: list[UnconfirmedOrderDTO]
