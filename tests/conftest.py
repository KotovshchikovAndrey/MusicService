from datetime import UTC, datetime
from io import BytesIO

import pytest

from adapters.driven.sql.models.user import User
from domain.models.builders.album import AlbumBuilder
from domain.models.builders.artist import ArtistBuilder
from domain.models.builders.track import TrackBuilder
from domain.models.builders.user import UserBuilder
from domain.models.entities.album import Album, AlbumInfo
from domain.models.entities.artist import Artist, BaseArtist
from domain.models.entities.track import PopularTrack, Track, TrackItem


@pytest.fixture(scope="function")
def datetime_mock() -> datetime:
    return datetime.now(UTC)


@pytest.fixture(scope="function")
def audio_mock() -> BytesIO:
    blob = BytesIO(b"12345")
    blob.size = 5
    return blob


@pytest.fixture(scope="function")
def album_mock(datetime_mock: datetime) -> Album:
    album = (
        AlbumBuilder()
        .set_title(title="Vmeste My")
        .set_cover(cover_url="/test_cover.png")
        .build()
    )

    album.created_at = datetime_mock
    return album


@pytest.fixture(scope="function")
def user_mock() -> User:
    user = UserBuilder().set_email(email="example@gmail.com").build()
    return user


@pytest.fixture(scope="function")
def artist_mock(user_mock: User) -> Artist:
    artist = (
        ArtistBuilder()
        .set_id(user_id=user_mock.id)
        .set_nickname(nickname="Unknown")
        .set_avatar(avatar_url="/avatar.png")
        .build()
    )

    return artist


@pytest.fixture(scope="function")
def track_mock(album_mock: Album) -> Track:
    track = (
        TrackBuilder()
        .set_album(album_id=album_mock.id)
        .set_title(title="In The End (Mellen Gi Remix)")
        .set_audio("/test_audio.mp3")
        .set_duration(4 * 60)
        .build()
    )

    return track


@pytest.fixture(scope="function")
def popular_track_mock(
    track_mock: Track,
    album_mock: Album,
    artist_mock: Artist,
) -> Track:
    popular_track = PopularTrack(
        id=track_mock.id,
        album_id=track_mock.album_id,
        title=track_mock.title,
        audio_url=track_mock.audio_url,
        duration=track_mock.duration,
        cover_url=album_mock.cover_url,
        artists=(BaseArtist(id=artist_mock.id, nickname=artist_mock.nickname),),
    )

    return popular_track


@pytest.fixture(scope="function")
def album_info_mock(
    album_mock: Album,
    artist_mock: Artist,
    track_mock: Track,
) -> AlbumInfo:
    track_item = TrackItem(
        id=track_mock.id,
        title=track_mock.title,
        audio_url=track_mock.audio_url,
        duration=track_mock.duration,
        album_id=album_mock.id,
        artists=(BaseArtist(id=artist_mock.id, nickname=artist_mock.nickname),),
    )

    album_info = AlbumInfo(
        id=album_mock.id,
        title=album_mock.title,
        cover_url=album_mock.cover_url,
        created_at=album_mock.created_at,
        tracks=(track_item,),
    )

    return album_info
