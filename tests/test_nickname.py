import pytest

from domain.models.values.nickname import Nickname


@pytest.mark.parametrize(
    "value",
    (
        "Andrey",  # Base nickname
        "Андрей",  # Russian nickname
        "Andrey12345",  # Nickname with digits
        "Andrey@*-=",  # Nickname with special symbols
    ),
)
def test_nickname_with_correct_value_then_success(value: str):
    nickname = Nickname(value)
    assert nickname.value == value


@pytest.mark.parametrize(
    "value",
    (
        "",  # Empty string
        "12345",  # Only digits
        "A" * 100,  # Too long
    ),
)
def test_nickname_with_incorrect_value_then_error(value: str):
    with pytest.raises(ValueError):
        Nickname(value)
