import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query

from application.dtos.order import CreateOrderDTO
from config.settings import settings
from domain.enums import OrderStatus
from presentation.api.dependencies import (
    AddOrderDep,
    CalculateTotalPriceDep,
    CurrentAdminIdDep,
    CurrentUserIdDep,
    GetAvailabilityDep,
    GetListMyOrdersDep,
    GetOrderDetailDep,
    ListOrdersDep,
    UpdateOrderStatusDep,
)
from presentation.api.schemas import (
    DayAvailabilityRead,
    OrderAdd,
    OrderRead,
    PriceCalculateRequest,
    PriceRead,
)
from presentation.api.schemas.order import (
    OrderDetailRead,
    OrderListRead,
    OrderStatusRead,
    OrderStatusUpdate,
)

router = APIRouter(
    prefix=settings.api_prefix.orders,
    tags=["Orders"],
)


@router.post("/total_price", response_model=PriceRead)
async def get_total_price(
    data: PriceCalculateRequest,
    use_case: CalculateTotalPriceDep,
):
    return await use_case.execute(
        weight_kg=data.weight_kg,
        filling_id=data.filling_id,
        decoration_id=data.decoration_id,
    )


@router.get(
    "/me",
    response_model=list[OrderRead],
)
async def list_my_orders(
    current_user_id: CurrentUserIdDep,
    use_case: GetListMyOrdersDep,
):
    return await use_case.execute(current_user_id)


@router.post("", response_model=OrderRead)
async def add_order(
    user_id: CurrentUserIdDep,
    data: OrderAdd,
    use_case: AddOrderDep,
):
    return await use_case.execute(CreateOrderDTO(user_id=user_id, **data.model_dump()))


@router.get("/availability", response_model=list[DayAvailabilityRead])
async def get_availability(
    date_from: date,
    date_to: date,
    use_case: GetAvailabilityDep,
):
    return await use_case.execute(date_from, date_to)


@router.get("", response_model=OrderListRead)
async def list_orders_for_admin(
    _: CurrentAdminIdDep,  # TODO: заменить на проверку админа
    use_case: ListOrdersDep,
    status: Annotated[list[OrderStatus] | None, Query()] = None,
    search: str | None = None,
    limit: int = Query(200, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return await use_case.execute(status, search, limit, offset)


@router.get("/{order_id}", response_model=OrderDetailRead)
async def get_order_detail(
    _: CurrentAdminIdDep,
    order_id: uuid.UUID,
    use_case: GetOrderDetailDep,
):
    return await use_case.execute(order_id)


@router.patch("/{order_id}/status", response_model=OrderStatusRead)
async def update_order_status(
    _: CurrentAdminIdDep,
    order_id: uuid.UUID,
    data: OrderStatusUpdate,
    use_case: UpdateOrderStatusDep,
):
    return await use_case.execute(order_id, data.status)
