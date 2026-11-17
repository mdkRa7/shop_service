import uuid

from pydantic import BaseModel


class DecorationBase(BaseModel):
    name: str
    price: int


class DecorationRead(DecorationBase):
    id: uuid.UUID


class DecorationAdd(DecorationBase):
    pass
