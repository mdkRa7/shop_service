from domain.exceptions import AppError


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
