from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from adapters.sql.mappers.album import map_to_album_entity, map_to_album_model
from adapters.sql.models.album import AlbumModel
from domain.entities.album import Album
from domain.repositories.album import AlbumRepository


class AlbumSqlRepository(AlbumRepository):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_new_releases(self, limit: int) -> list[Album]:
        stmt = select(AlbumModel).order_by(AlbumModel.created_at.desc()).limit(limit)
        models = await self._session.scalars(stmt)
        return [map_to_album_entity(model) for model in models]

    async def get_by_oid(
        self, album_oid: str, fetch_tracks: bool = False
    ) -> Album | None:
        stmt = select(AlbumModel).where(AlbumModel.oid == album_oid)
        if fetch_tracks:
            stmt = stmt.options(joinedload(AlbumModel.tracks))

        model = await self._session.scalar(stmt)
        if model is not None:
            return map_to_album_entity(model)

    async def upsert(self, album: Album) -> None:
        model = map_to_album_model(album)
        stmt = insert(AlbumModel).values(**model.get_upsert_values())
        stmt = stmt.on_conflict_do_update(
            index_elements=[AlbumModel.oid],
            set_=dict(stmt.excluded),
        )

        await self._session.execute(stmt)
