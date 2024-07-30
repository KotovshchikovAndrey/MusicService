import pytest

from domain.values.cover_url import CoverUrl


class TestCoverUrl:
    @pytest.mark.parametrize(
        "value",
        (
            "cover.png",
            "/",
            "/cover.mp4",
            "/cover.",
            f"/cover{"A" * 9_999}.jpg",
            "/cover.jpgA",
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

