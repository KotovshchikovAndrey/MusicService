from io import BytesIO
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.utils.blob import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork
from domain.values.audio_url import AudioUrl
from domain.values.avatar_url import AvatarUrl
from domain.values.cover_url import CoverUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.nickname import Nickname
from domain.values.oid import OID
from domain.values.title import Title
from tests.mocks.blob_storage import MockedBlobStorage
from tests.mocks.uow import MockedUnitOfWork


@pytest.fixture
def artist_mock() -> Artist:
    return Artist(
        nickname=Nickname("Unknown"),
        avatar_url=AvatarUrl("/avatar.png"),
    )


@pytest.fixture
def album_oid_mock() -> OID:
    return OID.generate()


@pytest.fixture
def track_mock(album_oid_mock, artist_mock: Artist) -> Track:
    return Track(
        album_oid=album_oid_mock,
        title=Title("In The End (Mellen Gi Remix)"),
        audio_url=AudioUrl("/test_audio.mp3"),
        duration=Duration(4 * 60),
        listens=Listens(0),
        cover_url=CoverUrl("/test_cover.png"),
        artists=(artist_mock,),
    )


@pytest.fixture
def album_mock(album_oid_mock: OID, track_mock: Track) -> Album:
    return Album(
        oid=album_oid_mock,
        title=Title("Vmeste My"),
        cover_url=CoverUrl("/test_cover.png"),
        tracks=(track_mock,),
    )


@pytest.fixture
def random_oid_mock() -> str:
    oid = OID.generate()
    return oid.value


@pytest.fixture
def audio_mock() -> BytesIO:
    blob = BytesIO(b"12345")
    blob.name = "test_audio.mp3"
    return blob


@pytest.fixture
def moderation_service_mock(audio_mock: BytesIO) -> ModerationServiceAdapter:
    mocked_moderation_service = MagicMock(spec=ModerationServiceAdapter)
    mocked_moderation_service.upload_approved_audio = AsyncMock(return_value=audio_mock)
    return mocked_moderation_service


@pytest.fixture
def uow_mock(album_mock: Album, artist_mock: Artist, track_mock: Track) -> UnitOfWork:
    return MockedUnitOfWork(
        tracks=[track_mock],
        albums=[album_mock],
        artists=[artist_mock],
    )


@pytest.fixture
def blob_storage_mock(audio_mock: BytesIO) -> BlobStorage:
    return MockedBlobStorage(blobs=[audio_mock])
