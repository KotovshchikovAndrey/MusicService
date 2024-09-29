import enum
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from domain.models.entities.base import BaseEntity


class TokenTTL(enum.IntEnum):
    ACCESS_TOKEN = 60 * 30  # 30 minutes
    REFRESH_TOKEN = 60 * 60 * 24 * 7  # 1 week


class TokenType(enum.StrEnum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"


@dataclass(eq=False, slots=True, kw_only=True)
class BaseToken(BaseEntity):
    token_type: TokenType
    owner_id: UUID
    expired_at: datetime
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def get_payload(self) -> dict:
        return {
            "jti": self.id.hex,
            "user_id": self.owner_id.hex,
            "iat": self.created_at.timestamp(),
            "exp": self.expired_at.timestamp(),
            "type": self.token_type.value,
        }

    @property
    def is_expired(self) -> bool:
        return datetime.now(UTC) >= self.expired_at

    @classmethod
    def from_payload(cls: type["BaseToken"], payload: dict) -> "BaseToken":
        return BaseToken(
            id=UUID(payload["jti"]),
            owner_id=UUID(payload["user_id"]),
            token_type=TokenType(payload["type"]),
            created_at=datetime.fromtimestamp(timestamp=payload["iat"], tz=UTC),
            expired_at=datetime.fromtimestamp(timestamp=payload["exp"], tz=UTC),
        )


@dataclass(eq=False, slots=True, kw_only=True)
class Token(BaseToken):
    device_id: str
    is_revoked: bool = field(default=False)
