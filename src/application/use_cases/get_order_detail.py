import uuid

from application.dtos import OrderDetailDTO
from application.exceptions import NotFoundError
from application.interfaces import OrderRepositoryProtocol


class GetOrderDetail:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self._order_repo = order_repo

    async def execute(self, order_id: uuid.UUID) -> OrderDetailDTO:
        result = await self._order_repo.get_detail(order_id)
        if result is None:
            raise NotFoundError("Order not found")
        order, filling_name, decoration_name = result
        return OrderDetailDTO(
            id=order.id,
            number=order.number,
            customer_name=order.customer_name,
            phone=order.phone,
            filling_name=filling_name,
            decoration_name=decoration_name,
            weight_kg=order.weight_kg,
            inscription=order.inscription,
            total_price=order.total_price,
            pickup_date=order.pickup_date,
            status=order.status,
            created_at=order.created_at,
        )
