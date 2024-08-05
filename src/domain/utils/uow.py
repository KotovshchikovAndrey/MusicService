from abc import ABC, abstractmethod
from typing import Self

from domain.repositories.album import AlbumRepository
from domain.repositories.artist import ArtistRepository
from domain.repositories.playlist import PlaylistRepository
from domain.repositories.track import TrackRepository


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
