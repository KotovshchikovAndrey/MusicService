from dataclasses import dataclass

from domain.models.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class Duration(BaseValue[int]):
    _max_seconds_duration = 60 * 5  # 5 minutes

    def validate(self) -> None:
        if self.value <= 0:
            raise ValueError(
                f"Invalid track duration '{self.value}'. Expected positive integer greater than 0"
            )

        if self.value > self._max_seconds_duration:
            raise ValueError(f"Too long track duration '{self.value}'")
