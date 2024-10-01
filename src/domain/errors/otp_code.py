from domain.errors.base import DomainError


class OTPCodeError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(error=OTPCodeError.__name__, message=message)


class InvalidOTPCodeError(OTPCodeError):
    def __init__(self) -> None:
        super().__init__(message="Invalid otp code")


class ExpiredOTPCodeError(InvalidOTPCodeError):
    def __init__(self) -> None:
        super().__init__()
