from dataclasses import asdict, fields

from application.dtos import CreateOrderDTO, OutputOrderDTO
from application.exceptions import (
    DayFullError,
    PickupDateTooSoonError,
    PriceMismatchError,
)
from application.interfaces import ActiveRepositoryProtocol, OrderRepositoryProtocol
from domain.constants import MAX_ORDERS_PER_DAY
from domain.enums import OrderStatus
from domain.services import calculate_total_price
from domain.services.pickup import earliest_pickup_date


class AddOrder:
    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        decoration_repo: ActiveRepositoryProtocol,
        filling_repo: ActiveRepositoryProtocol,
    ):
        self._order_repo = order_repo
        self._decoration_repo = decoration_repo
        self._filling_repo = filling_repo

    async def execute(self, dto: CreateOrderDTO) -> OutputOrderDTO:
        if dto.pickup_date < earliest_pickup_date():
            raise PickupDateTooSoonError()

        counts = await self._order_repo.counts_by_date_range(
            dto.pickup_date, dto.pickup_date
        )
        if counts.get(dto.pickup_date, 0) >= MAX_ORDERS_PER_DAY:
            raise DayFullError()

        decoration = 0
        if dto.decoration_id is not None:
            decoration = await self._decoration_repo.get_active_by_id(dto.decoration_id)
        filling = await self._filling_repo.get_active_by_id(dto.filling_id)
        total_price = calculate_total_price(
            weight_kg=dto.weight_kg,
            decoration=getattr(decoration, "price", 0),
            price_per_kg=filling.price_per_kg,
        )
        if total_price != dto.expected_price:
            raise PriceMismatchError()

        data = asdict(dto)
        data.pop("expected_price")
        data.update(status=OrderStatus.NEW, total_price=total_price)
        order = await self._order_repo.create(data)
        return OutputOrderDTO(
            **{f.name: getattr(order, f.name) for f in fields(OutputOrderDTO)}
        )
