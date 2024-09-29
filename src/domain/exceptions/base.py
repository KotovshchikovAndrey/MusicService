from utils.strings import to_snake_case


class BaseDomainException(Exception):
    exc_code: str
    detail: str

    def __init__(self, exc_code: str, detail: str) -> None:
        self.exc_code = exc_code
        self.detail = detail


class Unauthorized(BaseDomainException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(exc_code=Unauthorized.__name__, detail=detail)


class InvalidInput(BaseDomainException):
    def __init__(self, detail: str) -> None:
        super().__init__(exc_code=to_snake_case(InvalidInput.__name__), detail=detail)


class AccessDenied(BaseDomainException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(exc_code=to_snake_case(AccessDenied.__name__), detail=detail)


class NotFound(BaseDomainException):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(exc_code=to_snake_case(NotFound.__name__), detail=detail)


class Conflict(BaseDomainException):
    def __init__(self, detail: str) -> None:
        super().__init__(exc_code=to_snake_case(Conflict.__name__), detail=detail)
