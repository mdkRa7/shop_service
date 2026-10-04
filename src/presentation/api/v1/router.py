from fastapi import APIRouter

from config import settings

from .endpoints.healthcheck import router as healthcheck_router

router = APIRouter(prefix=settings.api_prefix.v1_prefix, tags=["V1"])

router.include_router(healthcheck_router)
