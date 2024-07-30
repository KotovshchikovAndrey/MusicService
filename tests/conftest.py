import pathlib
import typing as tp
import uuid
import aiofiles
import pytest
from unittest.mock import AsyncMock, MagicMock

from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.repositories.track import TrackRepository
from domain.utils.blob import BlobStorage
from domain.utils.uow import UnitOfWork
from domain.values.audio_url import AudioUrl
from domain.values.cover_url import CoverUrl
from domain.values.duration import Duration
from domain.values.fullname import FullName
from domain.values.title import Title


@pytest.fixture
def artist() -> Artist:
    return Artist(fullname=FullName("Unknown"))


@pytest.fixture
def track(artist: Artist) -> Track:
    return Track(
        title=Title("In The End (Mellen Gi Remix)"),
        audio_url=AudioUrl("/test_audio.mp3"),
        duration=Duration(4 * 60),
        artists={artist},
    )


@pytest.fixture
def album(track: Track) -> Album:
    return Album(
        title=Title("Vmeste My"),
        cover_url=CoverUrl("/test_cover.png"),
        tracks={track},
    )


@pytest.fixture
def random_oid() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def uow_mock(track: Track) -> UnitOfWork:
    uow_mock = MagicMock(spec=UnitOfWork)
    uow_mock.__aenter__.return_value = uow_mock
    uow_mock.commit = AsyncMock()
    uow_mock.rollback = AsyncMock()

    async def get_one(track_oid: str) -> Track | None:
        if track.oid == track_oid:
            return track

    tracks = MagicMock(spec=TrackRepository)
    tracks.get_one = get_one

    uow_mock.tracks = tracks
    return uow_mock


@pytest.fixture
def blob_storage_mock() -> BlobStorage:
    blob_storage_mock = MagicMock(spec=BlobStorage)

    async def read(blob_url: str, chunk_size: int) -> tp.AsyncGenerator[bytes, None]:
        path = pathlib.Path(".") / "media" / blob_url.replace("/", "")
        async with aiofiles.open(path, mode="rb") as io:
            while chunk := await io.read(chunk_size):
                yield chunk

    blob_storage_mock.read = read
    return blob_storage_mock
