from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from adapters.driven.sql.mappers.album import (
    map_to_album,
    map_to_album_info,
    map_to_insert_album_values,
)
from adapters.driven.sql.models.album import Album as AlbumModel
from adapters.driven.sql.models.track import Track as TrackModel
from domain.models.entities.album import Album, AlbumInfo
from domain.ports.driven.database.album_repository import AlbumRepository


class AlbumSQLRepository(AlbumRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_new_releases(self, limit: int) -> list[AlbumInfo]:
        stmt = (
            select(AlbumModel)
            .options(selectinload(AlbumModel.tracks).selectinload(TrackModel.artists))
            .order_by(AlbumModel.created_at.desc())
            .limit(limit)
        )

        models = await self._session.scalars(stmt)
        return [map_to_album_info(model) for model in models]

    async def get_by_id(self, album_id: UUID) -> Album | None:
        stmt = select(AlbumModel).where(AlbumModel.id == album_id)
        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_album(model)

    async def exists(self, album_id: UUID) -> bool:
        stmt = select(select(AlbumModel.id).where(AlbumModel.id == album_id).exists())
        result = await self._session.scalar(stmt)
        return bool(result)

    async def save(self, album: Album) -> None:
        values = map_to_insert_album_values(album)
        stmt = insert(AlbumModel).values(values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[AlbumModel.id],
            set_=dict(
                title=stmt.excluded.title,
                cover_url=stmt.excluded.cover_url,
            ),
        )

        await self._session.execute(stmt)
