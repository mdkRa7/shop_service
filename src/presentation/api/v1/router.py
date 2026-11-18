from fastapi import APIRouter

from config import settings

from .endpoints.dashboard import router as dashboard_router
from .endpoints.decoration import router as decoration_router
from .endpoints.filling import router as filling_router
from .endpoints.healthcheck import router as healthcheck_router
from .endpoints.order import router as order_router
from .endpoints.recipe import router as recipe_router

router = APIRouter(prefix=settings.api_prefix.v1_prefix, tags=["V1"])

router.include_router(healthcheck_router)
router.include_router(filling_router)
router.include_router(decoration_router)
router.include_router(order_router)
router.include_router(dashboard_router)
router.include_router(recipe_router)
