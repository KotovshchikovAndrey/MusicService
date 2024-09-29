from dataclasses import dataclass

from domain.models.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class Title(BaseValue[str]):
    _max_length = 70

    def validate(self) -> None:
        if not self.value:
            raise ValueError("Title cannot be an empty string")

        if len(self.value) > self._max_length:
            raise ValueError("Too long title")
