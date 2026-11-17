import uuid
from datetime import date

from sqlalchemy import func, or_, select

from domain.enums import OrderStatus
from infrastructure.database.models import Order

from ..models import Decoration, Filling
from .base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    model = Order

    async def orders_by_user(self, user_id: uuid.UUID) -> list[Order]:
        return await self.get_all(
            Order.user_id == user_id,
            order_by=[Order.created_at.desc()],
        )

    async def counts_by_date_range(
        self, date_from: date, date_to: date
    ) -> dict[date, int]:
        with self._db_errors("counts_by_date_range"):
            stmt = (
                select(Order.pickup_date, func.count())
                .where(
                    Order.pickup_date.between(date_from, date_to),
                    Order.status != OrderStatus.CANCELLED,
                )
                .group_by(Order.pickup_date)
            )
            rows = await self._session.execute(stmt)
            return {day: count for day, count in rows}

    async def list_filtered(
        self,
        statuses: list[OrderStatus],
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[Order, str]], int]:
        with self._db_errors("list_filtered"):
            conditions = [Order.status.in_(statuses)]
            if search:
                search_conditions = [
                    Order.customer_name.ilike(f"%{search}%"),
                ]

                digits = "".join(ch for ch in search if ch.isdigit())
                if digits:
                    search_conditions.append(Order.phone.ilike(f"%{digits}%"))

                if search.isdigit():
                    search_conditions.append(Order.number == int(search))

                conditions.append(or_(*search_conditions))

            stmt = (
                select(Order, Filling.name)
                .join(Filling, Filling.id == Order.filling_id)
                .where(*conditions)
                .order_by(Order.pickup_date, Order.number.desc())
                .limit(limit)
                .offset(offset)
            )
            total_stmt = select(func.count()).select_from(Order).where(*conditions)

            rows = (await self._session.execute(stmt)).all()
            total = await self._session.scalar(total_stmt)
            return [(row[0], row[1]) for row in rows], total or 0

    async def get_detail(
        self, order_id: uuid.UUID
    ) -> tuple[Order, str, str | None] | None:
        with self._db_errors("get_detail"):
            stmt = (
                select(Order, Filling.name, Decoration.name)
                .join(Filling, Filling.id == Order.filling_id)
                .outerjoin(Decoration, Decoration.id == Order.decoration_id)
                .where(Order.id == order_id)
            )
            row = (await self._session.execute(stmt)).first()
            if row is None:
                return None
            return row[0], row[1], row[2]
