class DomainException(Exception):
    detail: str

    def __init__(self, detail: str) -> None:
        self.message = detail


class BadRequestException(DomainException):
    def __init__(self, detail: str = "Invalid request params") -> None:
        super().__init__(detail)


class PermissionDeniedException(DomainException):
    def __init__(self, detail: str = "Permission denied") -> None:
        super().__init__(detail)


class NotFoundException(DomainException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(detail)


class ConflictException(DomainException):
    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(detail)
