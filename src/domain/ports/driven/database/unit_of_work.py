import logging
from abc import ABC, abstractmethod
from typing import Self

from domain.ports.driven.database.album_repository import AlbumRepository
from domain.ports.driven.database.artist_repository import ArtistRepository
from domain.ports.driven.database.otp_code_repository import OTPCodeRepository
from domain.ports.driven.database.playlist_repository import PlaylistRepository
from domain.ports.driven.database.token_repository import TokenRepository
from domain.ports.driven.database.track_repository import TrackRepository
from domain.ports.driven.database.user_repository import UserRepository


class UnitOfWork(ABC):
    tracks: TrackRepository
    playlists: PlaylistRepository
    albums: AlbumRepository
    artists: ArtistRepository
    users: UserRepository
    tokens: TokenRepository
    otp_codes: OTPCodeRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Exception | None, *args, **kwargs) -> None:
        if exc_type is not None:
            logging.exception(exc_type)
            await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
