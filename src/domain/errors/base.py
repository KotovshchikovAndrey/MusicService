class DomainError(Exception):
    error: str
    message: str

    def __init__(self, error: str, message: str) -> None:
        self.error = error
        self.message = message


class InvalidInputError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(error=InvalidInputError.__name__, message=message)


class NotFoundError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(error=NotFoundError.__name__, message=message)
