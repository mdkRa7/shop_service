from infrastructure.database.models import Recipe

from .base import BaseRepository


class RecipeRepository(BaseRepository[Recipe]):
    model = Recipe
