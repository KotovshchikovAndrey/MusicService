import re

from domain.models.values.base import BaseValue


class Email(BaseValue[str]):
    _max_length: int = 70
    _pattern: str = r"[A-Z-a-z_\d]+@(mail\.ru|gmail\.com)"

    def validate(self) -> None:
        if len(self.value) > self._max_length:
            raise ValueError("Too long email")

        if not re.fullmatch(self._pattern, self.value):
            raise ValueError("Invalid email format")
