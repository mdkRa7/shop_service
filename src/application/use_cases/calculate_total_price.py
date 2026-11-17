import uuid
from decimal import Decimal

from application.dtos import TotalPriceDTO
from application.interfaces import ActiveRepositoryProtocol
from domain.services import calculate_total_price


class CalculateTotalPrice:
    def __init__(
        self,
        filling_repo: ActiveRepositoryProtocol,
        decoration_repo: ActiveRepositoryProtocol,
    ):
        self._fillings_repo = filling_repo
        self._decoration_repo = decoration_repo

    async def execute(
        self, weight_kg: Decimal, filling_id: uuid.UUID, decoration_id: uuid.UUID | None
    ) -> TotalPriceDTO:
        filling = await self._fillings_repo.get_active_by_id(filling_id)
        decoration = 0

        if decoration_id is not None:
            decor = await self._decoration_repo.get_active_by_id(decoration_id)
            decoration = decor.price

        total_price = calculate_total_price(weight_kg, filling.price_per_kg, decoration)
        return TotalPriceDTO(total_price)
