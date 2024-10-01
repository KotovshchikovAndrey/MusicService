from datetime import datetime
from unittest.mock import patch

import pytest

from domain.models.builders.album import AlbumBuilder
from domain.models.entities.album import Album


class TestAlbum:
    @pytest.mark.parametrize(
        "title, cover_url",
        (
            (
                "Some album title",
                "/cover.png",
            ),
        ),
    )
    async def test_create_album_success(
        self,
        title: str,
        cover_url: str,
        mock_datetime: datetime,
    ) -> None:
        with patch("domain.models.entities.album.datetime") as mocker:
            mocker.now.return_value = mock_datetime
            new_album = (
                AlbumBuilder()
                .set_title(title=title)
                .set_cover(cover_url=cover_url)
                .build()
            )

            assert new_album.id is not None
            assert new_album.created_at is not None
            assert new_album.created_at == mock_datetime

            assert new_album.title.value == title
            assert new_album.cover_url.value == cover_url

    @pytest.mark.parametrize(
        "old_title, new_title, old_cover_url, new_cover_url",
        (
            (
                "Old album title",
                "New album title",
                "/old_cover.png",
                "/new_cover.png",
            ),
        ),
    )
    async def test_edit_property_success(
        self,
        old_title: str,
        new_title: str,
        old_cover_url: str,
        new_cover_url: str,
        mock_album: Album,
    ) -> None:
        mock_album.edit_title(new_title)
        mock_album.edit_cover(new_cover_url)

        assert mock_album.title.value != old_title
        assert mock_album.title.value == new_title

        assert mock_album.cover_url.value != old_cover_url
        assert mock_album.cover_url.value == new_cover_url
