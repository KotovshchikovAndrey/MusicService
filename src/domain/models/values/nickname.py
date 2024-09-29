from dataclasses import dataclass

from domain.models.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class Nickname(BaseValue[str]):
    _max_length = 70

    def validate(self) -> None:
        if not self.value:
            raise ValueError("Nickname cannot be an empty string")

        if len(self.value) > self._max_length:
            raise ValueError("Too long nickname")
