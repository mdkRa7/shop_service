from domain.exceptions import AppError


class PriceMismatchError(AppError):
    message = "The price has changed. Please review the updated price and confirm the order again."


class InvalidTokenTypeError(AppError):
    message = "This token type does not match"


class TokenValidationError(AppError):
    message = "Invalid token"


class DatabaseError(AppError):
    message = "Database failure"


class NotFoundError(AppError):
    message = "Not found"


class IntegrityConstraintError(AppError):
    message = "Resource conflict"


class InvalidDateRangeError(AppError):
    message = "Invalid date range"


class PickupDateTooSoonError(AppError):
    message = "Pickup date is too soon. Orders are accepted starting from tomorrow."


class DayFullError(AppError):
    message = "This day is fully booked. Please choose another date."
