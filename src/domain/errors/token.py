from domain.errors.base import DomainError


class TokenError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(error=TokenError.__name__, message=message)


class InvalidTokenError(TokenError):
    def __init__(self, message="Forbidden") -> None:
        super().__init__(message=message)


class ExpiredTokenError(InvalidTokenError):
    def __init__(self) -> None:
        super().__init__(message="Token has expired")


class InvalidRefreshTokenError(InvalidTokenError):
    def __init__(self) -> None:
        super().__init__()


class ExpiredRefreshTokenError(ExpiredTokenError):
    def __init__(self) -> None:
        super().__init__()


class RevokedRefreshTokenError(InvalidTokenError):
    def __init__(self) -> None:
        super().__init__()


class InvalidAccessTokenError(InvalidTokenError):
    def __init__(self) -> None:
        super().__init__()


class ExpiredAccessTokenError(ExpiredTokenError):
    def __init__(self) -> None:
        super().__init__()
