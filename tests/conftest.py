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
from domain.values.title import Title


@pytest.fixture(scope="function")
def datetime_mock() -> datetime:
    return datetime.now(UTC)


@pytest.fixture(scope="function")
def audio_mock() -> BytesIO:
    blob = BytesIO(b"12345")
    return blob


@pytest.fixture(scope="function")
def album_mock(datetime_mock: datetime) -> Album:
    return Album(
        title=Title("Vmeste My"),
        cover_url=CoverUrl("/test_cover.png"),
        created_at=datetime_mock,
    )


@pytest.fixture(scope="function")
def artist_mock() -> Artist:
    return Artist(
        nickname=Nickname("Unknown"),
        avatar_url=AvatarUrl("/avatar.png"),
    )


@pytest.fixture(scope="function")
def track_mock(album_mock: Album) -> Track:
    return Track(
        album_id=album_mock.id,
        title=Title("In The End (Mellen Gi Remix)"),
        audio_url=AudioUrl("/test_audio.mp3"),
        duration=Duration(4 * 60),
        listens=Listens(100),
    )


@pytest.fixture(scope="function")
def charted_track_mock(
    track_mock: Track,
    album_mock: Album,
    artist_mock: Artist,
) -> Track:
    return ChartedTrack(
        id=track_mock.id,
        album_id=track_mock.album_id,
        title=track_mock.title,
        audio_url=track_mock.audio_url,
        duration=track_mock.duration,
        cover_url=album_mock.cover_url,
        listens=track_mock.listens,
        artists=(
            ArtistLink(
                id=artist_mock.id,
                nickname=artist_mock.nickname,
            ),
        ),
    )


@pytest.fixture(scope="function")
def album_info_mock(
    album_mock: Album,
    artist_mock: Artist,
    track_mock: Track,
) -> AlbumInfo:
    return AlbumInfo(
        id=album_mock.id,
        title=album_mock.title,
        cover_url=album_mock.cover_url,
        created_at=album_mock.created_at,
        tracks=[
            TrackItem(
                id=track_mock.id,
                title=track_mock.title,
                duration=track_mock.duration,
                audio_url=track_mock.audio_url,
                listens=track_mock.listens,
                album_id=track_mock.album_id,
                artists=[
                    ArtistLink(
                        id=artist_mock.id,
                        nickname=artist_mock.nickname,
                    )
                ],
            )
        ],
    )
