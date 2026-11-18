import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Protocol, Sequence

from domain.enums import OrderStatus
from infrastructure.database.models import Order


class OrderRepositoryProtocol(Protocol):
    async def orders_by_user(self, *where: Any, order_by: Sequence[Any] = ()): ...
    async def create(self, data: dict[str, Any]): ...

    async def counts_by_date_range(
        self, date_from: date, date_to: date
    ) -> dict[date, int]: ...

    # async def list_filtered(
    #     self,
    #     statuses: list[OrderStatus],
    #     search: str | None,
    #     limit: int,
    #     offset: int,
    # ) -> tuple[list[tuple[Any, str]], int]: ...
    async def list_filtered(
        self,
        statuses: list[OrderStatus],
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[Any, str | None, str | None]], int]: ...

    async def get_detail(
        self,
        order_id: uuid.UUID,
    ) -> tuple[Any, str | None, str | None, str | None] | None: ...
    async def get_or_raise(self, obj_id: uuid.UUID): ...
    async def update(self, obj, data: dict[str, Any]): ...
    async def count_created(self, start: datetime, end: datetime) -> int: ...
    async def revenue_by_pickup_date(
        self, day: date, status: OrderStatus
    ) -> Decimal: ...

    async def list_by_status(
        self,
        status: OrderStatus,
    ) -> list[tuple[Any, str | None, str | None]]: ...
