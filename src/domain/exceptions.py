

class AppError(Exception):
    message: str

    def __init__(self, message: str | None = None):
        message = self.message if message is None else message
        super().__init__(message)


