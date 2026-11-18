from application.dtos import OrderListDTO, OrderListItemDTO
from application.interfaces import OrderRepositoryProtocol
from domain.enums import OrderStatus


class ListOrders:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self._order_repo = order_repo

    # async def execute(
    #     self,
    #     statuses: list[OrderStatus] | None,
    #     search: str | None,
    #     limit: int,
    #     offset: int,
    # ) -> OrderListDTO:
    #     rows, total = await self._order_repo.list_filtered(
    #         statuses or list(OrderStatus),
    #         search,
    #         limit,
    #         offset,
    #     )
    #     return OrderListDTO(
    #         total=total,
    #         items=[
    #             OrderListItemDTO(
    #                 id=order.id,
    #                 number=order.number,
    #                 customer_name=order.customer_name,
    #                 filling_name=filling_name,
    #                 pickup_date=order.pickup_date,
    #                 status=order.status,
    #             )
    #             for order, filling_name in rows
    #         ],
    #     )
    async def execute(
        self,
        status: list[OrderStatus] | None,
        search: str | None,
        limit: int,
        offset: int,
    ) -> OrderListDTO:
        rows, total = await self._order_repo.list_filtered(
            statuses=status or list(OrderStatus),
            search=search,
            limit=limit,
            offset=offset,
        )

        return OrderListDTO(
            total=total,
            items=[
                OrderListItemDTO(
                    id=order.id,
                    number=order.number,
                    customer_name=order.customer_name,
                    filling_name=filling_name,
                    recipe_name=recipe_name,
                    pickup_date=order.pickup_date,
                    status=order.status,
                )
                for order, filling_name, recipe_name in rows
            ],
        )
