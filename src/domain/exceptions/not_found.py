from domain.exceptions.base import DomainException


class NotFoundException(DomainException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(detail)
