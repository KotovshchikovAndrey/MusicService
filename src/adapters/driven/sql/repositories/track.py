from typing import Iterable, Literal
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from adapters.driven.sql import consts
from adapters.driven.sql.mappers.track import (
    map_to_charted_track,
    map_to_track,
    map_to_track_model,
)
from adapters.driven.sql.models.album import Album as AlbumModel
from adapters.driven.sql.models.artist import Artist as ArtistModel
from adapters.driven.sql.models.associations import track_artist
from adapters.driven.sql.models.track import Track as TrackModel
from domain.models.entities.track import ChartedTrack, Track
from domain.ports.driven.database.track_repository import TrackRepository


class TrackSqlRepository(TrackRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, track_id: UUID) -> Track | None:
        stmt = select(TrackModel).where(TrackModel.id == track_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_track(model)

    async def get_top_chart_for_period(
        self, period: Literal["all_time"] | Literal["day"], limit: int
    ) -> list[ChartedTrack]:
        stmt = (
            select(TrackModel)
            .options(
                joinedload(
                    TrackModel.artists,
                    innerjoin=True,
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

        result = await self._session.execute(stmt)
        models = result.unique().scalars()
        return [map_to_charted_track(model) for model in models]

    async def save(self, track: Track) -> None:
        model = map_to_track_model(track)
        stmt = insert(TrackModel).values(model.to_dict_values())
        stmt = stmt.on_conflict_do_update(
            index_elements=[TrackModel.id],
            set_=dict(title=stmt.excluded.title),
        )

        await self._session.execute(stmt)

    async def save_all(self, tracks: Iterable[Track]) -> None:
        if not tracks:
            return

        values = []
        for track in tracks:
            model = map_to_track_model(track)
            values.append(model.to_dict_values())

        stmt = insert(TrackModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[TrackModel.id],
            set_=dict(title=stmt.excluded.title),
        )

        await self._session.execute(stmt)

    async def set_artists(self, track_id: UUID, artist_ids: Iterable[UUID]) -> None:
        track_artist_values = []
        for artist_id in artist_ids:
            track_artist_value = dict(track_id=track_id, artist_id=artist_id)
            track_artist_values.append(track_artist_value)

        stmt = (
            insert(track_artist)
            .values(track_artist_values)
            .on_conflict_do_nothing(constraint=consts.TRACK_ARTIST_UNIQUE_CONSTRAINT)
        )

        await self._session.execute(stmt)

    async def increment_listens(self, track_id: UUID) -> None:
        stmt = (
            update(TrackModel)
            .where(TrackModel.id == track_id)
            .values(listens=TrackModel.listens + 1)
        )

        await self._session.execute(stmt)
