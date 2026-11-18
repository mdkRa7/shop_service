import uuid
from typing import Any

from application.dtos import RecipeDTO
from application.interfaces import RecipeRepositoryProtocol


def _to_dto(recipe) -> RecipeDTO:
    return RecipeDTO(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        price=recipe.price,
        image_url=recipe.image_url,
    )


class GetRecipes:
    def __init__(self, repo: RecipeRepositoryProtocol):
        self._repo = repo

    async def execute(self) -> list[RecipeDTO]:
        recipes = await self._repo.get_all()
        recipes.sort(key=lambda r: r.created_at, reverse=True)
        return [_to_dto(r) for r in recipes]


class GetRecipe:
    def __init__(self, repo: RecipeRepositoryProtocol):
        self._repo = repo

    async def execute(self, recipe_id: uuid.UUID) -> RecipeDTO:
        return _to_dto(await self._repo.get_or_raise(recipe_id))


class CreateRecipe:
    def __init__(self, repo: RecipeRepositoryProtocol):
        self._repo = repo

    async def execute(self, data: dict[str, Any]) -> RecipeDTO:
        return _to_dto(await self._repo.create(data))


class UpdateRecipe:
    def __init__(self, repo: RecipeRepositoryProtocol):
        self._repo = repo

    async def execute(self, recipe_id: uuid.UUID, data: dict[str, Any]) -> RecipeDTO:
        recipe = await self._repo.get_or_raise(recipe_id)
        if data:
            recipe = await self._repo.update(recipe, data)
        return _to_dto(recipe)


class DeleteRecipe:
    def __init__(self, repo: RecipeRepositoryProtocol):
        self._repo = repo

    async def execute(self, recipe_id: uuid.UUID) -> None:
        recipe = await self._repo.get_or_raise(recipe_id)
        await self._repo.delete(recipe)
