import uuid

from pydantic import BaseModel


class FillingBase(BaseModel):
    name: str
    price_per_kg: int


class FillingRead(FillingBase):
    id: uuid.UUID


class FillingAdd(FillingBase):
    pass
