import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class RecipeDTO:
    id: uuid.UUID
    name: str
    description: str
    price: Decimal
    image_url: str
