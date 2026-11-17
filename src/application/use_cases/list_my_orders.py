import uuid
from dataclasses import fields

from application.dtos import OutputOrderDTO
from application.interfaces import OrderRepositoryProtocol


class ListMyOrders:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self._order_repo = order_repo

    async def execute(
        self,
        user_id: uuid.UUID,
    ) -> list[OutputOrderDTO]:
        orders = await self._order_repo.orders_by_user(user_id)
        return [
            OutputOrderDTO(
                **{f.name: getattr(order, f.name) for f in fields(OutputOrderDTO)}
            )
            for order in orders
        ]
