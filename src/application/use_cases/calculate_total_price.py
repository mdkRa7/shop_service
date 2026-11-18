import uuid
from decimal import Decimal

from application.dtos import TotalPriceDTO
from application.interfaces import ActiveRepositoryProtocol, RecipeRepositoryProtocol
from domain.services import calculate_total_price


# class CalculateTotalPrice:
#     def __init__(
#         self,
#         filling_repo: ActiveRepositoryProtocol,
#         decoration_repo: ActiveRepositoryProtocol,
#     ):
#         self._fillings_repo = filling_repo
#         self._decoration_repo = decoration_repo
#
#     async def execute(
#         self, weight_kg: Decimal, filling_id: uuid.UUID, decoration_id: uuid.UUID | None
#     ) -> TotalPriceDTO:
#         filling = await self._fillings_repo.get_active_by_id(filling_id)
#         decoration = 0
#
#         if decoration_id is not None:
#             decor = await self._decoration_repo.get_active_by_id(decoration_id)
#             decoration = decor.price
#
#         total_price = calculate_total_price(weight_kg, filling.price_per_kg, decoration)
#         return TotalPriceDTO(total_price)
class CalculateTotalPrice:
    def __init__(
        self,
        filling_repo: ActiveRepositoryProtocol,
        decoration_repo: ActiveRepositoryProtocol,
        recipe_repo: RecipeRepositoryProtocol,
    ):
        self._fillings_repo = filling_repo
        self._decoration_repo = decoration_repo
        self._recipe_repo = recipe_repo

    async def execute(
        self,
        weight_kg: Decimal,
        recipe_id: uuid.UUID | None = None,
        filling_id: uuid.UUID | None = None,
        decoration_id: uuid.UUID | None = None,
    ) -> TotalPriceDTO:

        if recipe_id is not None:
            recipe = await self._recipe_repo.get_or_raise(recipe_id)

            total_price = calculate_total_price(
                weight_kg=weight_kg,
                price_per_kg=recipe.price,
            )

        else:
            filling = await self._fillings_repo.get_active_by_id(filling_id)

            decoration_price = Decimal("0")

            if decoration_id is not None:
                decoration = await self._decoration_repo.get_active_by_id(decoration_id)
                decoration_price = decoration.price

            total_price = calculate_total_price(
                weight_kg=weight_kg,
                price_per_kg=filling.price_per_kg,
                decoration=decoration_price,
            )

        return TotalPriceDTO(total_price)
