from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.sql.repositories.album import AlbumSqlRepository
from adapters.sql.repositories.playlist import PlaylistSqlRepository
from adapters.sql.repositories.track import TrackSqlRepository
from domain.utils.uow import UnitOfWork


class SqlUnitOfWork(UnitOfWork):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self) -> Self:
        self.tracks = TrackSqlRepository(session=self._session)
        self.playlists = PlaylistSqlRepository(session=self._session)
        self.albums = AlbumSqlRepository(session=self._session)

        return await super().__aenter__()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
