import pytest

from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track


class TestAlbum:
    async def test_create_album_success(self) -> None:
        title = "Excperemental Album"
        cover_url = "/cover.png"
        new_album = Album.create(title=title, cover_url=cover_url)

        assert new_album.oid is not None
        assert new_album.created_at is not None
        assert new_album.tracks is not None

        assert new_album.title.value == title
        assert new_album.cover_url.value == cover_url

    async def test_set_property_success(self, album_mock: Album) -> None:
        old_title = album_mock.title.value
        new_title = "New title"

        old_cover_url = album_mock.cover_url.value
        new_cover_url = "/new_cover.png"

        album_mock.change_title(new_title)
        album_mock.change_cover(new_cover_url)

        assert album_mock.title.value != old_title
        assert album_mock.title.value == new_title

        assert album_mock.cover_url.value != old_cover_url
        assert album_mock.cover_url.value == new_cover_url
