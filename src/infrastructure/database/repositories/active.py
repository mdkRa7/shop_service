import uuid

from application.exceptions import NotFoundError
from infrastructure.database import Base
from infrastructure.database.repositories.base import BaseRepository


class ActiveRepository[ModelT: Base](BaseRepository[ModelT]):
    """For models that have the is_active column."""

    async def get_active_by_id(self, obj_id: uuid.UUID) -> ModelT:
        obj = await self.get_or_raise(obj_id)

        if not obj.is_active:
            raise NotFoundError(f"{self.model.__name__} not found")
        return obj

    async def get_all_active(self) -> list[ModelT]:
        return await self.get_all(self.model.is_active.is_(True))
