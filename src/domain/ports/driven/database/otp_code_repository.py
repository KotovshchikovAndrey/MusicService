from typing import Protocol
from uuid import UUID

from domain.models.entities.otp_code import OTPCode, OTPCodePurpose


class OTPCodeRepository(Protocol):
    async def get_by_owner_and_purpose(
        self, owner_id: UUID, purpose: OTPCodePurpose
    ) -> OTPCode | None: ...

    async def save(self, otp_code: OTPCode) -> None: ...

    async def remove_by_id(self, otp_code_id: UUID) -> None: ...
