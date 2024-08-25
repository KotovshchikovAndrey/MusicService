from io import BytesIO
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.entities.album import Album, AlbumInfo
from domain.entities.artist import Artist
from domain.entities.track import ChartedTrack, Track
from domain.repositories.album import AlbumRepository
from domain.repositories.artist import ArtistRepository
from domain.repositories.track import TrackRepository
from domain.utils.blob_storage import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork


@pytest.fixture(scope="package")
def album_repository_mock(
    album_mock: Album,
    album_info_mock: AlbumInfo,
) -> AlbumRepository:
    repository = MagicMock(spec=AlbumRepository)
    repository.get_by_id = AsyncMock(return_value=album_mock)
    repository.upsert = AsyncMock()
    repository.get_new_releases = AsyncMock(return_value=[album_info_mock])
    return repository


@pytest.fixture(scope="package")
def artist_repository_mock(artist_mock: Artist) -> ArtistRepository:
    repository = MagicMock(spec=ArtistRepository)
    repository.get_by_id = AsyncMock(return_value=artist_mock)
    repository.filter_by_ids = AsyncMock(return_value=[artist_mock])
    repository.upsert = AsyncMock()
    return repository


@pytest.fixture(scope="package")
def blob_storage_mock(audio_mock: BytesIO) -> BlobStorage:
    blob_storage = MagicMock(spec=BlobStorage)

    async def audio_stream() -> AsyncGenerator[bytes, None]:
        for byte in audio_mock:
            yield byte

    blob_storage.read = MagicMock(return_value=audio_stream())
    blob_storage_mock.get_byte_size = AsyncMock(return_value=audio_mock.getvalue())
    return blob_storage


@pytest.fixture(scope="package")
def moderation_service_mock(audio_mock: BytesIO) -> ModerationServiceAdapter:
    mocked_moderation_service = MagicMock(spec=ModerationServiceAdapter)
    mocked_moderation_service.download_approved_audio = AsyncMock(
        return_value=audio_mock
    )

    return mocked_moderation_service


@pytest.fixture(scope="package")
def track_repository_mock(
    track_mock: Track,
    charted_track_mock: ChartedTrack,
) -> TrackRepository:
    repository = MagicMock(spec=TrackRepository)
    repository.get_by_id = AsyncMock(return_value=track_mock)
    repository.upsert = AsyncMock()
    repository.get_top_chart_for_period = AsyncMock(return_value=[charted_track_mock])
    return repository


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
