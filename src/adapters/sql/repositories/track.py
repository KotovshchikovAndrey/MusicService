from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from adapters.sql import consts
from adapters.sql.mappers.track import map_to_track_entity, map_to_track_model
from adapters.sql.models.track import TrackModel
from adapters.sql.models.associations import track_artist

from domain.entities.track import Track
from domain.entities.artist import Artist
from domain.repositories.track import TrackRepository


class TrackSqlRepository(TrackRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_oid(self, track_oid: str) -> Track | None:
        stmt = select(TrackModel).where(TrackModel.oid == track_oid)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_track_entity(model)

    async def get_popular(self, limit: int, offset: int) -> list[Track]: ...

    async def upsert(self, track: Track) -> None:
        model = map_to_track_model(track)
        stmt = insert(TrackModel).values(**model.get_sql_values())
        stmt = stmt.on_conflict_do_update(
            index_elements=[TrackModel.oid],
            set_=dict(stmt.excluded),
        )

        await self._session.execute(stmt)

    async def set_track_artists(self, track_oid: str, *artists: Artist) -> None:
        track_artist_values = []
        for artist in artists:
            track_artist_value = dict(track_id=track_oid, artist_id=artist.oid.value)
            track_artist_values.append(track_artist_value)

        stmt = insert(track_artist).values(track_artist_values)
        stmt = stmt.on_conflict_do_nothing(
            constraint=consts.TRACK_ARTIST_UNIQUE_CONSTRAINT
        )

        await self._session.execute(stmt)
