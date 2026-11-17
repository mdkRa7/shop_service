import uuid

import uuid_utils
from sqlalchemy.orm import Mapped, mapped_column


def _uuid7() -> uuid.UUID:
    return uuid.UUID(bytes=uuid_utils.uuid7().bytes)


class IdPkMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=_uuid7,
    )
