from dataclasses import dataclass
from domain.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class Description(BaseValue[str | None]):
    _max_length = 500

    def validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) > self._max_length:
            raise ValueError("Too long description")