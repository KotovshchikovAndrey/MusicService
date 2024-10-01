from datetime import UTC, datetime
from typing import Iterable, Literal
from uuid import UUID

from sqlalchemy import and_, exists, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from adapters.driven.sql import constraints
from adapters.driven.sql.mappers.track import (
    map_to_insert_track_values,
    map_to_popular_track,
    map_to_track,
)
from adapters.driven.sql.models.album import Album as AlbumModel
from adapters.driven.sql.models.artist import Artist as ArtistModel
from adapters.driven.sql.models.associations import listener, track_artist
from adapters.driven.sql.models.track import Track as TrackModel
from domain.models.entities.track import PopularTrack, Track
from domain.ports.driven.database.track_repository import TrackRepository


class TrackSQLRepository(TrackRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, track_id: UUID) -> Track | None:
        stmt = select(TrackModel).where(TrackModel.id == track_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_track(model)

    async def get_most_popular_for_period(
        self, period: Literal["all_time"] | Literal["day"], limit: int
    ) -> list[PopularTrack]:
        stmt = (
            select(TrackModel)
            .options(
                selectinload(
                    TrackModel.artists,
                ).load_only(
                    ArtistModel.id,
                    ArtistModel.nickname,
                ),
                joinedload(
                    TrackModel.album,
                    innerjoin=True,
                ).load_only(
                    AlbumModel.cover_url,
                ),
            )
            .limit(limit)
        )

        match period:
            case "all_time":
                stmt = stmt.order_by(TrackModel.listens.desc())
            case "day":
                stmt = stmt.order_by(TrackModel.listens_per_day.desc())

        models = await self._session.scalars(stmt)
        return [map_to_popular_track(model) for model in models]

    async def save(self, track: Track) -> None:
        values = map_to_insert_track_values(track)
        stmt = insert(TrackModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[TrackModel.id],
            set_=dict(title=stmt.excluded.title),
        )

        await self._session.execute(stmt)

    async def save_all(self, tracks: Iterable[Track]) -> None:
        if not tracks:
            return

        values_list = []
        for track in tracks:
            values = map_to_insert_track_values(track)
            values_list.append(values)

        stmt = insert(TrackModel).values(values_list)
        stmt = stmt.on_conflict_do_update(
            index_elements=[TrackModel.id],
            set_=dict(title=stmt.excluded.title),
        )

        await self._session.execute(stmt)

    async def specify_artists(self, track_id: UUID, artist_ids: Iterable[UUID]) -> None:
        values_list = []
        for artist_id in artist_ids:
            values = dict(track_id=track_id, artist_id=artist_id)
            values_list.append(values)

        stmt = (
            insert(track_artist)
            .values(values_list)
            .on_conflict_do_nothing(constraint=constraints.TRACK_ARTIST_UNIQUE_CONSTRAINT)
        )

        await self._session.execute(stmt)

    async def check_user_is_listener(self, track_id: UUID, user_id: UUID) -> bool:
        stmt = select(
            exists().where(
                and_(
                    listener.c.track_id == track_id,
                    listener.c.user_id == user_id,
                )
            )
        )

        return bool(await self._session.scalar(stmt))

    async def set_last_listened_date(self, track_id: UUID, user_id: UUID) -> None:
        values = {"track_id": track_id, "user_id": user_id}
        stmt = insert(listener).values(values)
        stmt = stmt.on_conflict_do_update(
            constraint=constraints.LISTENER_UNIQUE_CONSTRAINT,
            set_=dict(last_listened_at=datetime.now(UTC).replace(tzinfo=None)),
        )

        await self._session.execute(stmt)
