import pytest

from domain.models.builders.album import AlbumBuilder


@pytest.mark.parametrize(
    "old_title, new_title",
    (
        (
            "Old album title",
            "New album title",
        ),
    ),
)
async def test_edit_title_success(old_title: str, new_title: str) -> None:
    # Arrange
    album = AlbumBuilder().set_title(old_title).set_cover("/cover.png").build()

    # Act
    album.edit_title(new_title)

    # Assert
    assert album.title.value != old_title
    assert album.title.value == new_title


@pytest.mark.parametrize(
    "old_cover, new_cover",
    (
        (
            "/old_cover.png",
            "/new_cover.png",
        ),
    ),
)
async def test_edit_cover_success(old_cover: str, new_cover: str) -> None:
    # Arrange
    album = AlbumBuilder().set_title("My Album").set_cover(old_cover).build()

    # Act
    album.edit_cover(new_cover)

    # Assert
    assert album.cover_url.value != old_cover
    assert album.cover_url.value == new_cover
