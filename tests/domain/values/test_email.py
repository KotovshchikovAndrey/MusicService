import pytest

from domain.models.values.email import Email


class TestEmail:
    @pytest.mark.parametrize(
        "value",
        (
            "example@mail.ru",
            "example@gmail.com",
        ),
    )
    def test_valid_email(self, value: str) -> None:
        email = Email(value)
        assert email.value == value

    @pytest.mark.parametrize(
        "value",
        (
            "",
            "      ",
            "examplemail.ru",
            "example@gmail.lalala",
            "example@gmail.com".rjust(Email._max_length + 1, "a"),
        ),
    )
    def test_invalid_email(self, value: str) -> None:
        with pytest.raises(ValueError):
            Email(value)
