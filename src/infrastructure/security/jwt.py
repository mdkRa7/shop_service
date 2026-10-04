from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

from config.settings import settings

from application.exceptions import InvalidTokenTypeError, TokenValidationError


def check_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.jwt.public_key,
            algorithms=[settings.jwt.algorithm],
            options={"require": ["exp", "sub"]},
        )
    except InvalidTokenError:
        raise TokenValidationError()
    if payload.get("token_type") != "access":
        raise InvalidTokenTypeError()
    return payload
