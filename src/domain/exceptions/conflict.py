from domain.exceptions.base import DomainException


class ConflictException(DomainException):
    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(detail)
