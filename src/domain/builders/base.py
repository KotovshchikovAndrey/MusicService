from typing import Protocol
from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass(slots=True, init=False)
class BaseBuilder[T: BaseEntity](Protocol):
    def build(self) -> T: ...
