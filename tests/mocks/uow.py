from typing import Self

from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.utils.uow import UnitOfWork
from tests.mocks.album_repository import MockedAlbumRepository
from tests.mocks.artist_repository import MockedArtistRepository
from tests.mocks.track_repository import MockedTrackRepository


class MockedUnitOfWork(UnitOfWork):
    _tracks: list[Track]
    _albums: list[Album]
    _artists: list[Artist]

    def __init__(
        self,
        tracks: list[Track] = [],
        albums: list[Album] = [],
        artists: list[Artist] = [],
    ) -> None:
        self._tracks = tracks
        self._albums = albums
        self._artists = artists

    async def __aenter__(self) -> Self:
        self.tracks = MockedTrackRepository(tracks=self._tracks)
        self.albums = MockedAlbumRepository(albums=self._albums)
        self.artists = MockedArtistRepository(artists=self._artists)

        return await super().__aenter__()

    async def commit(self) -> None:
        return

    async def rollback(self) -> None:
        return
