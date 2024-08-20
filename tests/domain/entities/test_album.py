from datetime import UTC, datetime
from unittest.mock import patch

from domain.entities.album import Album
from domain.factories.album import AlbumFactory


class TestAlbum:
    async def test_create_album_success(self, datetime_mock: datetime) -> None:
        title = "Excperemental Album"
        cover_url = "/cover.png"

        with patch("domain.factories.album.datetime") as mocker:
            mocker.now.return_value = datetime_mock
            album_factory = AlbumFactory(title=title, cover_url=cover_url)
            new_album = album_factory.create()

            assert new_album.id is not None
            assert new_album.created_at is not None
            assert new_album.created_at == datetime_mock

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
