import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from application.exceptions import (
    AppError,
    DatabaseError,
    IntegrityConstraintError,
    InvalidTokenTypeError,
    NotFoundError,
    TokenValidationError,
)

log = logging.getLogger(__name__)

# One place that maps src errors to HTTP. Subclasses are matched via MRO.
ERROR_STATUS: dict[type[AppError], int] = {
    TokenValidationError: status.HTTP_401_UNAUTHORIZED,
    InvalidTokenTypeError: status.HTTP_401_UNAUTHORIZED,
    NotFoundError: status.HTTP_404_NOT_FOUND,
    IntegrityConstraintError: status.HTTP_409_CONFLICT,
    DatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        for cls in type(exc).__mro__:
            if cls in ERROR_STATUS:
                code = ERROR_STATUS[cls]
                break
        else:
            log.exception("Unmapped AppError", exc_info=exc)
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(status_code=code, content={"detail": str(exc)})
