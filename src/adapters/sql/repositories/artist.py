from typing import Iterable

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.sql.mappers.artist import map_to_artist, map_to_artist_model
from adapters.sql.models.artist import ArtistModel
from domain.entities.artist import Artist
from domain.repositories.artist import ArtistRepository


class ArtistSqlRepository(ArtistRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_oid(self, artist_oid: str) -> Artist | None:
        stmt = select(ArtistModel).where(ArtistModel.oid == artist_oid)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_artist(model)

    async def filter_by_oids(self, artist_oids: Iterable[str]) -> list[Artist]:
        stmt = select(ArtistModel).where(ArtistModel.oid.in_(artist_oids))
        models = await self._session.scalars(stmt)
        return [map_to_artist(model) for model in models]

    async def upsert(self, artist: Artist) -> None:
        model = map_to_artist_model(artist)
        stmt = insert(ArtistModel).values(model.get_values_to_upsert())
        stmt = stmt.on_conflict_do_update(
            index_elements=[ArtistModel.oid],
            set_=dict(stmt.excluded),
        )

        await self._session.execute(stmt)
