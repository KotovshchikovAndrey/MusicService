from io import BytesIO
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.models.entities.album import Album, AlbumInfo
from domain.models.entities.artist import Artist
from domain.models.entities.track import PopularTrack, Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.album_repository import AlbumRepository
from domain.ports.driven.database.artist_repository import ArtistRepository
from domain.ports.driven.database.track_repository import TrackRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader


@pytest.fixture(scope="function")
def album_repository_mock(
    album_mock: Album,
    album_info_mock: AlbumInfo,
) -> AlbumRepository:
    repository = MagicMock(spec=AlbumRepository)
    repository.get_by_id = AsyncMock(return_value=album_mock)
    repository.save = AsyncMock()
    repository.get_new_releases = AsyncMock(return_value=[album_info_mock])
    return repository


@pytest.fixture(scope="function")
def artist_repository_mock(artist_mock: Artist) -> ArtistRepository:
    repository = MagicMock(spec=ArtistRepository)
    repository.get_by_id = AsyncMock(return_value=artist_mock)
    repository.filter_by_ids = AsyncMock(return_value=[artist_mock])
    repository.save = AsyncMock()
    return repository


@pytest.fixture(scope="function")
def blob_storage_mock(audio_mock: BytesIO) -> BlobStorage:
    blob_storage = MagicMock(spec=BlobStorage)

    async def audio_stream() -> AsyncGenerator[bytes, None]:
        for byte in audio_mock:
            yield byte

    blob_storage.read = MagicMock(return_value=audio_stream())
    blob_storage.get_byte_size = AsyncMock(return_value=len(audio_mock.getvalue()))
    return blob_storage


@pytest.fixture(scope="function")
def file_downloader_mock(audio_mock: BytesIO) -> FileDownloader:
    file_downloader = MagicMock(spec=FileDownloader)
    file_downloader.download_by_url = AsyncMock(return_value=audio_mock)
    return file_downloader


@pytest.fixture(scope="function")
def track_repository_mock(
    track_mock: Track,
    popular_track_mock: PopularTrack,
) -> TrackRepository:
    repository = MagicMock(spec=TrackRepository)
    repository.get_by_id = AsyncMock(return_value=track_mock)
    repository.save = AsyncMock()
    repository.get_most_popular_for_period = AsyncMock(return_value=[popular_track_mock])
    return repository


@pytest.fixture(scope="function")
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
