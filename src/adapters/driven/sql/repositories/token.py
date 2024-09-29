from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.sql.mappers.token import map_to_insert_token_values, map_to_token
from adapters.driven.sql.models.token import Token as TokenModel
from domain.models.entities.token import Token
from domain.ports.driven.database.token_repository import TokenRepository


class TokenSQLRepository(TokenRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, token_id: UUID) -> Token | None:
        stmt = select(TokenModel).where(TokenModel.id == token_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_token(model)

    async def save(self, token: Token) -> None:
        values = map_to_insert_token_values(token)
        stmt = insert(TokenModel).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[TokenModel.id])
        await self._session.execute(stmt)

    async def revoke_by_owner_id(self, owner_id: UUID) -> None:
        raise NotImplementedError

    async def revoke_by_owner_id_and_device_id(
        self, owner_id: UUID, device_id: str
    ) -> None:
        raise NotImplementedError
