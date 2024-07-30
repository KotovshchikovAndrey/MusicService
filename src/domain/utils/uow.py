from abc import ABC, abstractmethod

from domain.repositories.album import AlbumRepository
from domain.repositories.playlist import PlaylistRepository
from domain.repositories.track import TrackRepository


class UnitOfWork(ABC):
    tracks: TrackRepository
    playlists: PlaylistRepository
    albums: AlbumRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
