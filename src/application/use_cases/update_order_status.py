import uuid

from application.dtos.order import OrderStatusDTO
from application.interfaces import OrderRepositoryProtocol
from domain.enums import OrderStatus


class UpdateOrderStatus:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self._order_repo = order_repo

    async def execute(
        self, order_id: uuid.UUID, new_status: OrderStatus
    ) -> OrderStatusDTO:
        order = await self._order_repo.get_or_raise(order_id)
        order = await self._order_repo.update(order, {"status": new_status})
        return OrderStatusDTO(id=order.id, status=order.status)
