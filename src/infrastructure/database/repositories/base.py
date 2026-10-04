import logging
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import DatabaseError, IntegrityConstraintError, NotFoundError
from infrastructure.database.base import Base


log = logging.getLogger(__name__)



class BaseRepository[ModelT: Base]:
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @contextmanager
    def _db_errors(self, operation: str) -> Iterator[None]:
        try:
            yield
        except IntegrityError as e:
            log.warning("Integrity error in %s.%s: %s", self.model.__name__, operation, e.orig)
            raise IntegrityConstraintError() from e
        except SQLAlchemyError as e:
            log.exception("DB error in %s.%s", self.model.__name__, operation)
            raise DatabaseError() from e

    async def get(self, obj_id: uuid.UUID) -> ModelT | None:
        with self._db_errors("get"):
            return await self._session.get(self.model, obj_id)

    async def get_or_raise(self, obj_id: uuid.UUID) -> ModelT:
        obj = await self.get(obj_id)
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} not found")
        return obj

    async def create(self, data: dict[str, Any]) -> ModelT:
        with self._db_errors("create"):
            obj = self.model(**data)
            self._session.add(obj)
            await self._session.flush()
            return obj

    async def update(self, obj: ModelT, data: dict[str, Any]) -> ModelT:
        with self._db_errors("update"):
            for field, value in data.items():
                setattr(obj, field, value)
            await self._session.flush()
            return obj

    async def update_by_id(self, obj_id: uuid.UUID, data: dict[str, Any]) -> ModelT | None:
        with self._db_errors("update_by_id"):
            stmt = (
                update(self.model)
                .where(self.model.id == obj_id)
                .values(**data)
                .returning(self.model)
            )
            return await self._session.scalar(stmt)


    async def delete(self, obj: ModelT) -> None:
        with self._db_errors("delete"):
            await self._session.delete(obj)
            await self._session.flush()
