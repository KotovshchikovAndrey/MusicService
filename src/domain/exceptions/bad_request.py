from domain.exceptions.base import DomainException


class BadRequestException(DomainException):
    def __init__(self, detail: str = "Invalid request params") -> None:
        super().__init__(detail)
