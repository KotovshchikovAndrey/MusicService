from typing import AsyncGenerator
import pathlib
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
from domain.values.nickname import Nickname
from domain.values.oid import OID
from domain.values.title import Title


@pytest.fixture
def artist() -> Artist:
    return Artist(nickname=Nickname("Unknown"))


@pytest.fixture
def album_oid() -> OID:
    return OID.generate()


@pytest.fixture
def track(album_oid, artist: Artist) -> Track:
    return Track(
        album_oid=album_oid,
        title=Title("In The End (Mellen Gi Remix)"),
        audio_url=AudioUrl("/test_audio.mp3"),
        duration=Duration(4 * 60),
        artists=(artist,),
    )


@pytest.fixture
def album(album_oid: OID, track: Track) -> Album:
    return Album(
        oid=album_oid,
        title=Title("Vmeste My"),
        cover_url=CoverUrl("/test_cover.png"),
        tracks=(track,),
    )


@pytest.fixture
def random_oid() -> str:
    oid = OID.generate()
    return oid.value


@pytest.fixture
def uow_mock(track: Track) -> UnitOfWork:
    uow_mock = MagicMock(spec=UnitOfWork)
    uow_mock.__aenter__.return_value = uow_mock
    uow_mock.commit = AsyncMock()
    uow_mock.rollback = AsyncMock()

    async def get_by_oid(track_oid: str) -> Track | None:
        if track.oid == track_oid:
            return track

    tracks = MagicMock(spec=TrackRepository)
    tracks.get_by_oid = get_by_oid

    uow_mock.tracks = tracks
    return uow_mock


@pytest.fixture
def blob_storage_mock() -> BlobStorage:
    blob_storage_mock = MagicMock(spec=BlobStorage)

    async def read(
        blob_url: str,
        chunk_size: int,
        start_byte: int = 0,
        end_byte: int | None = None,
    ) -> AsyncGenerator[bytes, None]:
        path = pathlib.Path(".") / "media" / blob_url.replace("/", "")
        async with aiofiles.open(path, mode="rb") as io:
            await io.seek(start_byte)
            while chunk := await io.read(chunk_size):
                yield chunk

    async def get_byte_size(blob_url: str) -> int:
        path = pathlib.Path(".") / "media" / blob_url.replace("/", "")
        return path.stat().st_size

    blob_storage_mock.read = read
    blob_storage_mock.get_byte_size = get_byte_size
    return blob_storage_mock
