from domain.exceptions.base import AccessDenied


class InvalidOTPCode(AccessDenied):
    def __init__(self) -> None:
        super().__init__()


class ExpiredOTPCode(AccessDenied):
    def __init__(self) -> None:
        super().__init__()
