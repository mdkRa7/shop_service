from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class DayAvailabilityDTO:
    day: date
    is_available: bool
    free_slots: int
