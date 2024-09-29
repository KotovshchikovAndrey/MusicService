from dataclasses import dataclass

from domain.models.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class Duration(BaseValue[int]):
    _max_seconds_duration = 60 * 5  # 5 minutes

    def validate(self) -> None:
        if self.value <= 0:
            raise ValueError("Duration cannot be a negative number")

        if self.value > self._max_seconds_duration:
            raise ValueError("Too long duration")
