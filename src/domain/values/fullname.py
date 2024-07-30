from dataclasses import dataclass
from domain.values.base import BaseValue


@dataclass(frozen=True, slots=True)
class FullName(BaseValue[str]):
    _max_length = 70

    def validate(self) -> None:
        if not self.value:
            raise ValueError("Fullname should not be an empty string")

        if len(self.value) > self._max_length:
            raise ValueError(f"Too long fullname '{self.value}'")
