import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class FillingDTO:
    id: uuid.UUID
    name: str
    price_per_kg: int
