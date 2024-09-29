from typing import Self

from adapters.driven.sql.connection import SQLDatabaseConnection
from adapters.driven.sql.repositories.album import AlbumSQLRepository
from adapters.driven.sql.repositories.artist import ArtistSQLRepository
from adapters.driven.sql.repositories.otp_code import OTPCodeSQLRepository
from adapters.driven.sql.repositories.playlist import PlaylistSQLRepository
from adapters.driven.sql.repositories.token import TokenSQLRepository
from adapters.driven.sql.repositories.track import TrackSQLRepository
from adapters.driven.sql.repositories.user import UserSQLRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork


class SQLUnitOfWork(UnitOfWork):
    _database: SQLDatabaseConnection

    def __init__(self, database: SQLDatabaseConnection) -> None:
        self._database = database

    async def __aenter__(self) -> Self:
        self._session = self._database.get_scoped_session()
        self.tracks = TrackSQLRepository(session=self._session)
        self.playlists = PlaylistSQLRepository(session=self._session)
        self.albums = AlbumSQLRepository(session=self._session)
        self.artists = ArtistSQLRepository(session=self._session)
        self.users = UserSQLRepository(session=self._session)
        self.tokens = TokenSQLRepository(session=self._session)
        self.otp_codes = OTPCodeSQLRepository(session=self._session)

        return await super().__aenter__()

    async def __aexit__(self, exc_type: Exception | None, *args, **kwargs) -> None:
        await super().__aexit__(exc_type, *args, **kwargs)
        await self._session.remove()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
