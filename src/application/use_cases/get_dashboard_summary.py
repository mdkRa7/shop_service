from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from application.dtos import DashboardSummaryDTO, UnconfirmedOrderDTO
from application.interfaces import OrderRepositoryProtocol
from domain.constants import SHOP_TIMEZONE
from domain.enums import OrderStatus


class GetDashboardSummary:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self._order_repo = order_repo

    async def execute(self) -> DashboardSummaryDTO:
        tz = ZoneInfo(SHOP_TIMEZONE)
        today = datetime.now(tz).date()
        start = datetime.combine(today, time.min, tzinfo=tz)
        end = start + timedelta(days=1)

        new_count = await self._order_repo.count_created(start, end)
        revenue = await self._order_repo.revenue_by_pickup_date(today, OrderStatus.DONE)
        rows = await self._order_repo.list_by_status(OrderStatus.NEW)

        return DashboardSummaryDTO(
            day=today,
            new_orders_count=new_count,
            revenue=revenue,
            unconfirmed_count=len(rows),
            unconfirmed=[
                UnconfirmedOrderDTO(
                    id=order.id,
                    number=order.number,
                    customer_name=order.customer_name,
                    filling_name=filling_name,
                    recipe_name=recipe_name,
                    pickup_date=order.pickup_date,
                )
                for order, filling_name, recipe_name in rows
            ],
        )

    # async def execute(self) -> DashboardSummaryDTO:
    # tz = ZoneInfo(SHOP_TIMEZONE)
    # today = datetime.now(tz).date()
    # start = datetime.combine(today, time.min, tzinfo=tz)
    # end = start + timedelta(days=1)
    #
    # new_count = await self._order_repo.count_created(start, end)
    # revenue = await self._order_repo.revenue_by_pickup_date(
    #     today, OrderStatus.DONE
    # )
    # rows = await self._order_repo.list_by_status(OrderStatus.NEW)
    #
    # return DashboardSummaryDTO(
    #     day=today,
    #     new_orders_count=new_count,
    #     revenue=revenue,
    #     unconfirmed_count=len(rows),
    #     unconfirmed=[
    #         UnconfirmedOrderDTO(
    #             id=order.id,
    #             number=order.number,
    #             customer_name=order.customer_name,
    #             filling_name=filling_name,
    #             pickup_date=order.pickup_date,
    #         )
    #         for order, filling_name in rows
    #     ],
    # )
