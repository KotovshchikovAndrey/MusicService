from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from adapters.sql.mappers.artist import map_to_artist, map_to_artist_model
from adapters.sql.models.artist import ArtistModel
from domain.entities.artist import Artist
from domain.repositories.artist import ArtistRepository


class ArtistSqlRepository(ArtistRepository):
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

    async def upsert(self, artist: Artist) -> None:
        model = map_to_artist_model(artist)
        stmt = insert(ArtistModel).values(model.get_values_to_upsert())
        stmt = stmt.on_conflict_do_update(
            index_elements=[ArtistModel.id],
            set_=dict(stmt.excluded),
        )

        await self._session.execute(stmt)
