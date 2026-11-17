import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class DecorationDTO:
    id: uuid.UUID
    name: str
    price: int
