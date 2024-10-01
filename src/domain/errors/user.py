from domain.errors.base import DomainError, NotFoundError


class AuthenticationError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            error=AuthenticationError.__name__,
            message="User is not authenticated",
        )


class UserNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(message="User not found")
