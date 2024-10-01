import pytest

from domain.models.values.cover_url import CoverUrl


class TestCoverUrl:
    @pytest.mark.parametrize(
        "value",
        (
            "cover.png",
            "/",
            "/cover.mp4",
            "/cover.",
            "/cover.jpgA",
            "/cover.jpg".rjust(CoverUrl._max_length + 1, "a"),
        ),
    )
    async def test_invalid_cover_url(self, value: str) -> None:
        with pytest.raises(ValueError):
            CoverUrl(value)

    @pytest.mark.parametrize(
        "value",
        (
            "/cover.png",
            "/cover.jpg",
            "/cover.jpeg",
            "/test_cover.jpeg",
            "/test-cover.jpeg",
        ),
    )
    async def test_valid_cover_url(self, value: str) -> None:
        cover_url = CoverUrl(value)
        assert cover_url.value == value
