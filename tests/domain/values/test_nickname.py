import pytest

from domain.models.values.nickname import Nickname


class TestNickname:
    @pytest.mark.parametrize(
        "value",
        (
            "XXMan",
            "Artist boy",
            "SuperNinja228",
        ),
    )
    def test_valid_nickname(self, value: str) -> None:
        nickname = Nickname(value)
        assert nickname.value == value

    @pytest.mark.parametrize(
        "value",
        (
            "",
            "           ",
            "192192",
            "Artist_1".ljust(Nickname._max_length + 1, "0"),
        ),
    )
    def test_invalid_nickname(self, value: str) -> None:
        with pytest.raises(ValueError):
            Nickname(value)
