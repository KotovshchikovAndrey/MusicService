from dataclasses import dataclass

from domain.models.entities.otp_code import OTPCode
from domain.models.entities.user import User


@dataclass(frozen=True)
class Event: ...


@dataclass(frozen=True)
class UserSignedIn(Event):
    user: User
    otp_code: OTPCode
