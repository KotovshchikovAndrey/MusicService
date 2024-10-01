import enum
import random
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from domain.errors.otp_code import ExpiredOTPCodeError, InvalidOTPCodeError
from domain.models.entities.base import BaseEntity


class OTPCodePurpose(enum.StrEnum):
    VERIFY = "verify"


@dataclass(eq=False, slots=True, kw_only=True)
class OTPCode(BaseEntity):
    code: int
    owner_id: UUID
    purpose: OTPCodePurpose
    expired_at: datetime

    def check(self, code: int) -> None:
        if self.code != code:
            raise InvalidOTPCodeError()

        if self.is_expired:
            raise ExpiredOTPCodeError()

    @property
    def is_expired(self) -> bool:
        return self.expired_at <= datetime.now(UTC)

    @staticmethod
    def generate_code(length: int = 4) -> None:
        code = [str(random.randint(1, 9)) for _ in range(length)]
        return int("".join(code))
