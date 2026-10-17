from enum import StrEnum


class OrderStatus(StrEnum):
    NEW = "new"
    CONFIRMED = "confirmed"
    READY = "ready"
    DONE = "done"
    CANCELLED = "cancelled"
