from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.repositories.album import AlbumRepository
from domain.repositories.artist import ArtistRepository
from domain.repositories.track import TrackRepository
from domain.utils.uow import UnitOfWork


@pytest.fixture(scope="package")
def uow_mock(
    album_repository_mock: AlbumRepository,
    artist_repository_mock: ArtistRepository,
    track_repository_mock: TrackRepository,
) -> UnitOfWork:
    uow = MagicMock(spec=UnitOfWork)
    uow.__aenter__.return_value = uow

    uow.albums = album_repository_mock
    uow.tracks = track_repository_mock
    uow.artists = artist_repository_mock

    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    return uow
