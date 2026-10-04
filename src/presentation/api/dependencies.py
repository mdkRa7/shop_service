

import uuid
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import TokenValidationError
from infrastructure.security.jwt import check_access_token
from infrastructure.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


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


AccessTokenDep = Annotated[str, Depends(get_access_token)]
CurrentUserIdDep = Annotated[uuid.UUID, Depends(get_current_user_id)]
