import uuid
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import TokenValidationError
from application.use_cases import (
    AddOrder,
    CalculateTotalPrice,
    GetDecorations,
    GetFillings,
    ListMyOrders,
)
from application.use_cases.get_availability import GetAvailability
from application.use_cases.get_dashboard_summary import GetDashboardSummary
from application.use_cases.get_order_detail import GetOrderDetail
from application.use_cases.list_admin_routers import ListOrders
from application.use_cases.recipes import (
    CreateRecipe,
    DeleteRecipe,
    GetRecipe,
    GetRecipes,
    UpdateRecipe,
)
from application.use_cases.update_order_status import UpdateOrderStatus
from infrastructure.database import get_session
from infrastructure.database.repositories import (
    DecorationRepository,
    FillingRepository,
    OrderRepository,
    RecipeRepository,
)
from infrastructure.security.jwt import check_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_filling_repo(session: SessionDep):
    return FillingRepository(session)


def get_decoration_repo(session: SessionDep):
    return DecorationRepository(session)


def get_order_repo(session: SessionDep):
    return OrderRepository(session)


def get_recipe_repo(session: SessionDep):
    return RecipeRepository(session)


FillingRepoDep = Annotated[FillingRepository, Depends(get_filling_repo)]
DecorationRepoDep = Annotated[DecorationRepository, Depends(get_decoration_repo)]
OrderRepoDep = Annotated[OrderRepository, Depends(get_order_repo)]
RecipeRepoDep = Annotated[RecipeRepository, Depends(get_recipe_repo)]


def get_access_token(
    token: Annotated[str | None, Cookie(alias="access_token")] = None,
) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return token


def get_current_user_id(
    token: Annotated[str, Depends(get_access_token)],
) -> uuid.UUID:
    payload = check_access_token(token)
    try:
        return uuid.UUID(payload["sub"])
    except (ValueError, TypeError) as e:
        raise TokenValidationError() from e


def get_current_admin_id(
    token: Annotated[str, Depends(get_access_token)],
) -> uuid.UUID:
    payload = check_access_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    try:
        return uuid.UUID(payload["sub"])
    except (ValueError, TypeError) as e:
        raise TokenValidationError() from e


def get_add_order_use_case(
    order_repo: OrderRepoDep,
    decoration_repo: DecorationRepoDep,
    filling_repo: FillingRepoDep,
    recipe_repo: RecipeRepoDep,
) -> AddOrder:
    return AddOrder(
        order_repo=order_repo,
        filling_repo=filling_repo,
        decoration_repo=decoration_repo,
        recipe_repo=recipe_repo,
    )


def get_availability_use_case(repo: OrderRepoDep) -> GetAvailability:
    return GetAvailability(repo)


def get_list_my_orders_use_case(repo: OrderRepoDep) -> ListMyOrders:
    return ListMyOrders(repo)


def get_decoration_use_case(repo: DecorationRepoDep) -> GetDecorations:
    return GetDecorations(repo)


def get_fillings_use_case(repo: FillingRepoDep) -> GetFillings:
    return GetFillings(repo)


def get_order_detail_use_case(repo: OrderRepoDep) -> GetOrderDetail:
    return GetOrderDetail(repo)


def calculate_total_price_use_case(
    filling_repo: FillingRepoDep,
    decoration_repo: DecorationRepoDep,
    recipe_repo: RecipeRepoDep,
) -> CalculateTotalPrice:
    return CalculateTotalPrice(filling_repo, decoration_repo, recipe_repo)


def get_list_orders_use_case(repo: OrderRepoDep) -> ListOrders:
    return ListOrders(repo)


def get_update_order_status_use_case(repo: OrderRepoDep) -> UpdateOrderStatus:
    return UpdateOrderStatus(repo)


def get_dashboard_summary_use_case(repo: OrderRepoDep) -> GetDashboardSummary:
    return GetDashboardSummary(repo)


RecipeRepoDep = Annotated[RecipeRepository, Depends(get_recipe_repo)]


def get_recipes_use_case(repo: RecipeRepoDep) -> GetRecipes:
    return GetRecipes(repo)


def get_recipe_use_case(repo: RecipeRepoDep) -> GetRecipe:
    return GetRecipe(repo)


def create_recipe_use_case(repo: RecipeRepoDep) -> CreateRecipe:
    return CreateRecipe(repo)


def update_recipe_use_case(repo: RecipeRepoDep) -> UpdateRecipe:
    return UpdateRecipe(repo)


def delete_recipe_use_case(repo: RecipeRepoDep) -> DeleteRecipe:
    return DeleteRecipe(repo)


GetRecipesDep = Annotated[GetRecipes, Depends(get_recipes_use_case)]
GetRecipeDep = Annotated[GetRecipe, Depends(get_recipe_use_case)]
CreateRecipeDep = Annotated[CreateRecipe, Depends(create_recipe_use_case)]
UpdateRecipeDep = Annotated[UpdateRecipe, Depends(update_recipe_use_case)]
DeleteRecipeDep = Annotated[DeleteRecipe, Depends(delete_recipe_use_case)]
GetDashboardSummaryDep = Annotated[
    GetDashboardSummary, Depends(get_dashboard_summary_use_case)
]
UpdateOrderStatusDep = Annotated[
    UpdateOrderStatus, Depends(get_update_order_status_use_case)
]
GetOrderDetailDep = Annotated[GetOrderDetail, Depends(get_order_detail_use_case)]
ListOrdersDep = Annotated[ListOrders, Depends(get_list_orders_use_case)]
GetAvailabilityDep = Annotated[GetAvailability, Depends(get_availability_use_case)]
AddOrderDep = Annotated[AddOrder, Depends(get_add_order_use_case)]
GetListMyOrdersDep = Annotated[ListMyOrders, Depends(get_list_my_orders_use_case)]
CalculateTotalPriceDep = Annotated[
    CalculateTotalPrice, Depends(calculate_total_price_use_case)
]
GetDecorationDep = Annotated[GetDecorations, Depends(get_decoration_use_case)]
GetFillingsDep = Annotated[GetFillings, Depends(get_fillings_use_case)]
AccessTokenDep = Annotated[str, Depends(get_access_token)]
CurrentUserIdDep = Annotated[uuid.UUID, Depends(get_current_user_id)]
CurrentAdminIdDep = Annotated[uuid.UUID, Depends(get_current_admin_id)]
