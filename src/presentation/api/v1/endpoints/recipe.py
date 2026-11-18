import uuid

from fastapi import APIRouter, status

from config.settings import settings
from presentation.api.dependencies import (
    CreateRecipeDep,
    CurrentAdminIdDep,
    DeleteRecipeDep,
    GetRecipeDep,
    GetRecipesDep,
    UpdateRecipeDep,
)
from presentation.api.schemas.recipe import RecipeCreate, RecipeRead, RecipeUpdate

router = APIRouter(
    prefix=settings.api_prefix.recipes,
    tags=["Recipes"],
)


@router.get("", response_model=list[RecipeRead])
async def list_recipes(use_case: GetRecipesDep):
    return await use_case.execute()


@router.get("/{recipe_id}", response_model=RecipeRead)
async def get_recipe(recipe_id: uuid.UUID, use_case: GetRecipeDep):
    return await use_case.execute(recipe_id)


@router.post("", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    _: CurrentAdminIdDep,
    data: RecipeCreate,
    use_case: CreateRecipeDep,
):
    return await use_case.execute(data.model_dump())


@router.patch("/{recipe_id}", response_model=RecipeRead)
async def update_recipe(
    _: CurrentAdminIdDep,
    recipe_id: uuid.UUID,
    data: RecipeUpdate,
    use_case: UpdateRecipeDep,
):
    return await use_case.execute(recipe_id, data.model_dump(exclude_unset=True))


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    _: CurrentAdminIdDep,
    recipe_id: uuid.UUID,
    use_case: DeleteRecipeDep,
):
    await use_case.execute(recipe_id)
