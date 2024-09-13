from abc import ABC, abstractmethod
from typing import Self

from domain.ports.driven.database.album_repository import AlbumRepository
from domain.ports.driven.database.artist_repository import ArtistRepository
from domain.ports.driven.database.playlist_repository import PlaylistRepository
from domain.ports.driven.database.track_repository import TrackRepository


class UnitOfWork(ABC):
    tracks: TrackRepository
    playlists: PlaylistRepository
    albums: AlbumRepository
    artists: ArtistRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
