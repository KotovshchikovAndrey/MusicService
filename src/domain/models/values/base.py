import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BaseValue[TValue](ABC):
    value: TValue

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None: ...


@dataclass(frozen=True, slots=True)
class Url(BaseValue[str]):
    _max_length = 255

    def validate(self) -> None:
        if len(self.value) > self._max_length:
            raise ValueError("Too long url")

        if not re.fullmatch(self.get_pattern(), self.value):
            raise ValueError("Invalid url format")

    @abstractmethod
    def get_pattern(self) -> str: ...
