from typing import Iterable
from uuid import UUID

from sqlalchemy import exists, select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from adapters.driven.sql.mappers.artist import (
    map_to_artist,
    map_to_insert_artist_values,
)
from adapters.driven.sql.models.artist import Artist as ArtistModel
from domain.models.entities.artist import Artist
from domain.ports.driven.database.artist_repository import ArtistRepository


class ArtistSQLRepository(ArtistRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        stmt = select(ArtistModel).where(ArtistModel.id == artist_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_artist(model)

    async def get_list(self, limit: int, offset: int) -> list[Artist]:
        stmt = select(ArtistModel).limit(limit).offset(offset)
        models = await self._session.scalars(stmt)
        return [map_to_artist(model) for model in models]

    async def get_total_count(self) -> int:
        stmt = select(func.count()).select_from(ArtistModel)
        total_count: int = await self._session.scalar(stmt)
        return total_count

    async def filter_by_ids(self, artist_ids: Iterable[UUID]) -> list[Artist]:
        stmt = select(ArtistModel).where(ArtistModel.id.in_(artist_ids))
        models = await self._session.scalars(stmt)
        return [map_to_artist(model) for model in models]

    async def save(self, artist: Artist) -> None:
        values = map_to_insert_artist_values(artist)
        stmt = insert(ArtistModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[ArtistModel.id],
            set_=dict(
                nickname=stmt.excluded.nickname,
                avatar_url=stmt.excluded.avatar_url,
            ),
        )

        await self._session.execute(stmt)

    async def exists_all(self, artist_ids: Iterable[UUID]) -> bool:
        stmt = select(func.count(ArtistModel.id)).where(ArtistModel.id.in_(artist_ids))
        model_count = bool(await self._session.scalar(stmt))
        return len(artist_ids) == model_count
