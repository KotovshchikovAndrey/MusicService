import asyncio
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


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mock_datetime() -> datetime:
    return datetime.now(UTC)


@pytest.fixture(scope="session")
def mock_audio() -> BytesIO:
    blob = BytesIO(b"12345")
    blob.size = 5
    return blob


@pytest.fixture(scope="session")
def mock_album(mock_datetime: datetime) -> Album:
    album = (
        AlbumBuilder()
        .set_title(title="Vmeste My")
        .set_cover(cover_url="/test_cover.png")
        .build()
    )

    album.created_at = mock_datetime
    return album


@pytest.fixture(scope="session")
def mock_user() -> User:
    user = UserBuilder().set_email(email="example@gmail.com").build()
    return user


@pytest.fixture(scope="session")
def mock_artist(mock_user: User) -> Artist:
    artist = (
        ArtistBuilder()
        .set_id(user_id=mock_user.id)
        .set_nickname(nickname="Unknown")
        .set_avatar(avatar_url="/avatar.png")
        .build()
    )

    return artist


@pytest.fixture(scope="session")
def mock_track(mock_album: Album) -> Track:
    track = (
        TrackBuilder()
        .set_album(album_id=mock_album.id)
        .set_title(title="In The End (Mellen Gi Remix)")
        .set_audio("/test_audio.mp3")
        .set_duration(4 * 60)
        .build()
    )

    return track


@pytest.fixture(scope="session")
def mock_popular_track(
    mock_track: Track,
    mock_album: Album,
    mock_artist: Artist,
) -> Track:
    popular_track = PopularTrack(
        id=mock_track.id,
        album_id=mock_track.album_id,
        title=mock_track.title,
        audio_url=mock_track.audio_url,
        duration=mock_track.duration,
        cover_url=mock_album.cover_url,
        artists=(BaseArtist(id=mock_artist.id, nickname=mock_artist.nickname),),
    )

    return popular_track


@pytest.fixture(scope="session")
def mock_album_info(
    mock_album: Album,
    mock_artist: Artist,
    mock_track: Track,
) -> AlbumInfo:
    track_item = TrackItem(
        id=mock_track.id,
        title=mock_track.title,
        audio_url=mock_track.audio_url,
        duration=mock_track.duration,
        album_id=mock_album.id,
        artists=(BaseArtist(id=mock_artist.id, nickname=mock_artist.nickname),),
    )

    album_info = AlbumInfo(
        id=mock_album.id,
        title=mock_album.title,
        cover_url=mock_album.cover_url,
        created_at=mock_album.created_at,
        tracks=(track_item,),
    )

    return album_info
