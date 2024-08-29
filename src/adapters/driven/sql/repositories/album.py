from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from adapters.driven.sql.mappers.album import (
    map_to_album,
    map_to_album_info,
    map_to_album_model,
)
from adapters.driven.sql.models.album import AlbumModel
from adapters.driven.sql.models.track import TrackModel
from domain.entities.album import Album, AlbumInfo
from domain.repositories.album import AlbumRepository


class AlbumSqlRepository(AlbumRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_new_releases(self, limit: int) -> list[AlbumInfo]:
        stmt = (
            select(AlbumModel)
            .options(
                joinedload(
                    AlbumModel.tracks,
                    innerjoin=True,
                ).joinedload(
                    TrackModel.artists,
                    innerjoin=True,
                ),
            )
            .order_by(AlbumModel.created_at.desc())
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        models = result.unique().scalars()
        return [map_to_album_info(model) for model in models]

    async def get_by_id(self, album_id: UUID) -> Album | None:
        stmt = select(AlbumModel).where(AlbumModel.id == album_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_album(model)

    async def check_exists(self, album_id: UUID) -> bool:
        stmt = select(select(AlbumModel.id).where(AlbumModel.id == album_id).exists())

        result = await self._session.scalar(stmt)
        return bool(result)

    async def save(self, album: Album) -> None:
        model = map_to_album_model(album)
        stmt = insert(AlbumModel).values(model.to_dict_values())
        stmt = stmt.on_conflict_do_update(
            index_elements=[AlbumModel.id],
            set_=dict(
                title=stmt.excluded.title,
                cover_url=stmt.excluded.cover_url,
            ),
        )

        await self._session.execute(stmt)
