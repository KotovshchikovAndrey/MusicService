from datetime import UTC, datetime
from io import BytesIO

import pytest

from domain.models.builders.album import AlbumBuilder
from domain.models.builders.artist import ArtistBuilder
from domain.models.builders.track import TrackBuilder
from domain.models.entities.album import Album, AlbumInfo
from domain.models.entities.artist import Artist, BaseArtist
from domain.models.entities.track import ChartedTrack, Track, TrackItem
from domain.models.values.listens import Listens


@pytest.fixture(scope="function")
def datetime_mock() -> datetime:
    return datetime.now(UTC)


@pytest.fixture(scope="function")
def audio_mock() -> BytesIO:
    blob = BytesIO(b"12345")
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
def artist_mock() -> Artist:
    artist = (
        ArtistBuilder()
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

    track.listens = Listens(100)
    return track


@pytest.fixture(scope="function")
def charted_track_mock(
    track_mock: Track,
    album_mock: Album,
    artist_mock: Artist,
) -> Track:
    charted_track = ChartedTrack(id=track_mock.id)
    charted_track.album_id = track_mock.album_id
    charted_track.title = track_mock.title
    charted_track.audio_url = track_mock.audio_url
    charted_track.duration = track_mock.duration
    charted_track.cover_url = album_mock.cover_url
    charted_track.listens = track_mock.listens

    base_artist = BaseArtist(id=artist_mock.id)
    base_artist.nickname = artist_mock.nickname

    charted_track.artists = (base_artist,)
    return charted_track


@pytest.fixture(scope="function")
def album_info_mock(
    album_mock: Album,
    artist_mock: Artist,
    track_mock: Track,
) -> AlbumInfo:
    album_info = AlbumInfo(id=album_mock.id)
    album_info.title = album_mock.title
    album_info.cover_url = album_mock.cover_url
    album_info.created_at = album_mock.created_at

    track_item = TrackItem(id=track_mock.id)
    track_item.title = track_mock.title
    track_item.duration = track_mock.duration
    track_item.audio_url = track_mock.audio_url
    track_item.listens = track_mock.listens
    track_item.album_id = track_mock.album_id

    base_artist = BaseArtist(id=artist_mock.id)
    base_artist.nickname = artist_mock.nickname
    track_item.artists = (base_artist,)

    album_info.tracks = (track_item,)
    return album_info
