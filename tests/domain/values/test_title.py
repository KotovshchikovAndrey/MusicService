import pytest

from domain.values.title import Title


class TestTitle:
    async def test_too_long_title(self) -> None:
        with pytest.raises(ValueError):
            Title("A" * 9_999)

    async def test_empty_title(self) -> None:
        with pytest.raises(ValueError):
            Title("")

    async def test_valid_title(self) -> None:
        value = "In The End"
        title = Title(value)
        assert title.value == value
