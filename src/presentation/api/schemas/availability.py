from datetime import date

from pydantic import BaseModel


class DayAvailabilityBase(BaseModel):
    day: date
    is_available: bool
    free_slots: int


class DayAvailabilityRead(DayAvailabilityBase):
    pass
