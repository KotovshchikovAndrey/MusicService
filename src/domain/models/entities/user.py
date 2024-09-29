from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from domain.models.entities.base import BaseEntity
from domain.models.entities.otp_code import OTPCode, OTPCodePurpose
from domain.models.entities.token import BaseToken, Token, TokenTTL, TokenType
from domain.models.values.email import Email


@dataclass(eq=False, slots=True, kw_only=True)
class BaseUser(BaseEntity):
    email: Email
    is_active: bool = field(default=False)


@dataclass(eq=False, slots=True, kw_only=True)
class AuthenticatedUser(BaseUser):
    token: BaseToken


@dataclass(eq=False, slots=True, kw_only=True)
class User(BaseUser):
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def request_new_otp_code(self, purpose: OTPCodePurpose, ttl: int = 60 * 3) -> OTPCode:
        return OTPCode(
            code=OTPCode.generate_code(),
            owner_id=self.id,
            purpose=purpose,
            expired_at=datetime.now(UTC) + timedelta(seconds=ttl),
        )

    def issue_token_pair(self, device_id: str) -> tuple[Token, Token]:
        access_token = Token(
            owner_id=self.id,
            device_id=device_id,
            token_type=TokenType.ACCESS_TOKEN,
            expired_at=datetime.now(UTC) + timedelta(seconds=TokenTTL.ACCESS_TOKEN),
        )

        refresh_token = Token(
            owner_id=self.id,
            device_id=device_id,
            token_type=TokenType.REFRESH_TOKEN,
            expired_at=datetime.now(UTC) + timedelta(seconds=TokenTTL.REFRESH_TOKEN),
        )

        return access_token, refresh_token
