from datetime import date, timedelta

from application.dtos import DayAvailabilityDTO
from application.exceptions import InvalidDateRangeError
from application.interfaces import OrderRepositoryProtocol
from domain.constants import MAX_CALENDAR_RANGE_DAYS, MAX_ORDERS_PER_DAY
from domain.services.pickup import earliest_pickup_date


class GetAvailability:
    def __init__(self, order_repo: OrderRepositoryProtocol):
        self._order_repo = order_repo

    async def execute(self, date_from: date, date_to: date) -> list[DayAvailabilityDTO]:
        if date_from > date_to or (date_to - date_from).days > MAX_CALENDAR_RANGE_DAYS:
            raise InvalidDateRangeError()

        counts = await self._order_repo.counts_by_date_range(date_from, date_to)
        earliest = earliest_pickup_date()

        result = []
        for i in range((date_to - date_from).days + 1):
            day = date_from + timedelta(days=i)
            booked = counts.get(day, 0)
            free_slots = 0 if day < earliest else max(0, MAX_ORDERS_PER_DAY - booked)
            result.append(
                DayAvailabilityDTO(
                    day=day, free_slots=free_slots, is_available=free_slots > 0
                )
            )
        return result
