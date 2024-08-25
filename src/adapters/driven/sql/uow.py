from typing import Self

from adapters.driven.sql.connection import SqlDatabaseConnection
from adapters.driven.sql.repositories.album import AlbumSqlRepository
from adapters.driven.sql.repositories.artist import ArtistSqlRepository
from adapters.driven.sql.repositories.playlist import PlaylistSqlRepository
from adapters.driven.sql.repositories.track import TrackSqlRepository
from domain.utils.uow import UnitOfWork


class SqlUnitOfWork(UnitOfWork):
    _database: SqlDatabaseConnection

    def __init__(self, database: SqlDatabaseConnection) -> None:
        self._database = database

    async def __aenter__(self) -> Self:
        self._session = self._database.get_scoped_session()
        self.tracks = TrackSqlRepository(session=self._session)
        self.playlists = PlaylistSqlRepository(session=self._session)
        self.albums = AlbumSqlRepository(session=self._session)
        self.artists = ArtistSqlRepository(session=self._session)

        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs) -> None:
        await super().__aexit__(*args, **kwargs)
        await self._session.remove()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
