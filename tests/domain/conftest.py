from io import BytesIO
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.album_repository import AlbumRepository
from domain.ports.driven.database.artist_repository import ArtistRepository
from domain.ports.driven.database.track_repository import TrackRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.file_downloader import FileDownloader


@pytest.fixture(scope="function")
def mock_blob_storage() -> BlobStorage:
    blob_storage = MagicMock(spec=BlobStorage)
    return blob_storage


@pytest.fixture(scope="function")
def mock_file_downloader(mock_audio: BytesIO) -> FileDownloader:
    file_downloader = MagicMock(spec=FileDownloader)
    file_downloader.download_by_url = AsyncMock(return_value=mock_audio)
    return file_downloader


@pytest.fixture(scope="function")
def mock_uow() -> UnitOfWork:
    uow = MagicMock(spec=UnitOfWork)
    uow.__aenter__.return_value = uow

    uow.albums = MagicMock(spec=AlbumRepository)
    uow.tracks = MagicMock(spec=TrackRepository)
    uow.artists = MagicMock(spec=ArtistRepository)

    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    return uow
