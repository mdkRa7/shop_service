from infrastructure.database.models import Recipe

from .active import ActiveRepository


class RecipeRepository(ActiveRepository[Recipe]):
    model = Recipe
