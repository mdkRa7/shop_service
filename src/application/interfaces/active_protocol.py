import uuid
from typing import Protocol


class ActiveRepositoryProtocol(Protocol):
    async def get_all_active(self) -> list: ...
    async def get_active_by_id(self, obj_id: uuid.UUID): ...
