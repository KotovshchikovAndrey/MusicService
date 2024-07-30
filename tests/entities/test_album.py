import pytest

from domain.entities.album import Album
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.exceptions.permission_denied import PermissionDeniedException
from domain.values.cover_url import CoverUrl
from domain.values.title import Title


class TestAlbum:
    async def test_create_album_success(self, track: Track) -> None:
        title = "Excperemental Album"
        cover_url = "/cover.png"

        new_album = Album(title=Title(title), cover_url=CoverUrl(cover_url))

        assert new_album.oid is not None
        assert new_album.created_at is not None
        assert new_album.tracks is not None

        assert new_album.title.value == title
        assert new_album.cover_url.value == cover_url

    async def test_set_property_success(self, album: Album, artist: Artist) -> None:
        old_title = album.title.value
        new_title = "New title"

        old_cover_url = album.cover_url.value
        new_cover_url = "/new_cover.png"

        album.set_title(new_title, my_oid=artist.oid)
        album.set_cover(new_cover_url, my_oid=artist.oid)

        assert album.title.value != old_title
        assert album.title.value == new_title

        assert album.cover_url.value != old_cover_url
        assert album.cover_url.value == new_cover_url

    async def test_set_property_when_user_is_not_artist(
        self, album: Album, random_oid: str
    ) -> None:
        old_title = album.title.value
        new_title = "New title"

        old_cover_url = album.cover_url.value
        new_cover_url = "/new_cover.png"

        with pytest.raises(PermissionDeniedException):
            album.set_title(new_title, my_oid=random_oid)
            album.set_cover(new_cover_url, my_oid=random_oid)

            assert album.title.value == old_title
            assert album.cover_url.value == old_cover_url
