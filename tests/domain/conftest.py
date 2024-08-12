from datetime import UTC, datetime
from io import BytesIO

import pytest

from domain.entities.album import Album, AlbumInfo
from domain.entities.artist import Artist, ArtistLink
from domain.entities.track import ChartedTrack, Track, TrackItem
from domain.values.audio_url import AudioUrl
from domain.values.avatar_url import AvatarUrl
from domain.values.cover_url import CoverUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.nickname import Nickname
from domain.values.oid import OID
from domain.values.title import Title
from tests.domain.mocks import *


@pytest.fixture(scope="package")
def datetime_mock() -> datetime:
    return datetime.now(UTC)


@pytest.fixture(scope="package")
def random_oid_mock() -> str:
    oid = OID.generate()
    return oid.value


@pytest.fixture(scope="package")
def audio_mock() -> BytesIO:
    blob = BytesIO(b"12345")
    blob.name = "test_audio.mp3"
    return blob


@pytest.fixture(scope="package")
def album_mock(datetime_mock: datetime) -> Album:
    return Album(
        title=Title("Vmeste My"),
        cover_url=CoverUrl("/test_cover.png"),
        created_at=datetime_mock,
    )


@pytest.fixture(scope="package")
def artist_mock() -> Artist:
    return Artist(
        nickname=Nickname("Unknown"),
        avatar_url=AvatarUrl("/avatar.png"),
    )


@pytest.fixture(scope="package")
def track_mock(album_mock: Album) -> Track:
    return Track(
        album_oid=album_mock.oid,
        title=Title("In The End (Mellen Gi Remix)"),
        audio_url=AudioUrl("/test_audio.mp3"),
        duration=Duration(4 * 60),
        listens=Listens(100),
    )


@pytest.fixture(scope="package")
def charted_track_mock(
    track_mock: Track,
    album_mock: Album,
    artist_mock: Artist,
) -> Track:
    return ChartedTrack(
        oid=track_mock.oid,
        album_oid=track_mock.album_oid,
        title=track_mock.title,
        audio_url=track_mock.audio_url,
        duration=track_mock.duration,
        cover_url=album_mock.cover_url,
        listens=track_mock.listens,
        artists=(
            ArtistLink(
                oid=artist_mock.oid,
                nickname=artist_mock.nickname,
            ),
        ),
    )


@pytest.fixture(scope="package")
def album_info_mock(
    album_mock: Album,
    artist_mock: Artist,
    track_mock: Track,
) -> AlbumInfo:
    return AlbumInfo(
        oid=album_mock.oid,
        title=album_mock.title,
        cover_url=album_mock.cover_url,
        created_at=album_mock.created_at,
        tracks=[
            TrackItem(
                oid=track_mock.oid,
                title=track_mock.title,
                duration=track_mock.duration,
                audio_url=track_mock.audio_url,
                listens=track_mock.listens,
                album_oid=track_mock.album_oid,
                artists=[
                    ArtistLink(
                        oid=artist_mock.oid,
                        nickname=artist_mock.nickname,
                    )
                ],
            )
        ],
    )
