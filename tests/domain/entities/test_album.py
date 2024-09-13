from datetime import datetime
from unittest.mock import patch

from domain.models.builders.album import AlbumBuilder
from domain.models.entities.album import Album


class TestAlbum:
    async def test_create_album_success(self, datetime_mock: datetime) -> None:
        title = "Excperemental Album"
        cover_url = "/cover.png"

        with patch("domain.models.entities.album.datetime") as mocker:
            mocker.now.return_value = datetime_mock
            new_album = (
                AlbumBuilder()
                .set_title(title=title)
                .set_cover(cover_url=cover_url)
                .build()
            )

            assert new_album.id is not None
            assert new_album.created_at is not None
            assert new_album.created_at == datetime_mock

            assert new_album.title.value == title
            assert new_album.cover_url.value == cover_url

    async def test_edit_property_success(self, album_mock: Album) -> None:
        old_title = album_mock.title.value
        new_title = "New title"

        old_cover_url = album_mock.cover_url.value
        new_cover_url = "/new_cover.png"

        album_mock.edit_title(new_title)
        album_mock.edit_cover(new_cover_url)

        assert album_mock.title.value != old_title
        assert album_mock.title.value == new_title

        assert album_mock.cover_url.value != old_cover_url
        assert album_mock.cover_url.value == new_cover_url
