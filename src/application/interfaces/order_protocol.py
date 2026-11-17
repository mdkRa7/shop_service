import uuid
from datetime import date
from typing import Any, Protocol, Sequence

from domain.enums import OrderStatus


class OrderRepositoryProtocol(Protocol):
    async def orders_by_user(self, *where: Any, order_by: Sequence[Any] = ()): ...
    async def create(self, data: dict[str, Any]): ...

    async def counts_by_date_range(
        self, date_from: date, date_to: date
    ) -> dict[date, int]: ...
    async def list_filtered(
        self,
        statuses: list[OrderStatus],
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[Any, str]], int]: ...
    async def get_detail(
        self, order_id: uuid.UUID
    ) -> tuple[Any, str, str | None] | None: ...
    async def get_or_raise(self, obj_id: uuid.UUID): ...
    async def update(self, obj, data: dict[str, Any]): ...
