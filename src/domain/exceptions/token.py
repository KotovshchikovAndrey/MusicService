from domain.exceptions.base import AccessDenied, Unauthorized


class RevokedRefreshToken(AccessDenied):
    def __init__(self) -> None:
        super().__init__()


class InvalidRefreshToken(AccessDenied):
    def __init__(self) -> None:
        super().__init__()


class ExpiredRefreshToken(AccessDenied):
    def __init__(self) -> None:
        super().__init__(detail="Token has expired")


class ExpiredAccessToken(Unauthorized):
    def __init__(self) -> None:
        super().__init__(detail="Token has expired")


class InvalidAccessToken(Unauthorized):
    def __init__(self) -> None:
        super().__init__()
