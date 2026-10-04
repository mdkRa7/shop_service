import logging

from config.logging import setup_root_logger
from infrastructure.database.engine import dispose
from infrastructure.clients import redis
from contextlib import asynccontextmanager

import uvicorn
from presentation.api.exception_handlers import register_exception_handlers
from presentation.api.v1 import router
from config import settings
from fastapi import FastAPI




@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await redis.aclose()
    await dispose()

app = FastAPI(lifespan=lifespan)
setup_root_logger(level=logging.INFO)
register_exception_handlers(app)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:src",
        host=settings.api_conf.host,
        port=settings.api_conf.port,
        reload=True,
    )
