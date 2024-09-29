from typing import Protocol
from uuid import UUID

from domain.models.entities.token import Token


class TokenRepository(Protocol):
    async def get_by_id(self, token_id: UUID) -> Token | None: ...

    async def save(self, token: Token) -> None: ...

    async def revoke_by_owner_id(self, owner_id: UUID) -> None: ...

    async def revoke_by_owner_id_and_device_id(
        self, owner_id: UUID, device_id: str
    ) -> None: ...
