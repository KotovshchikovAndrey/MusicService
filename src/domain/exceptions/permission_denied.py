from domain.exceptions.base import DomainException


class PermissionDeniedException(DomainException):
    def __init__(self, detail: str = "Permission denied") -> None:
        super().__init__(detail)
