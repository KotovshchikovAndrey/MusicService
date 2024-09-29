from dataclasses import dataclass
from typing import Protocol

from domain.models.entities.base import BaseEntity


@dataclass(eq=False, init=False, slots=True)
class BaseBuilder[T: BaseEntity](Protocol):
    def build(self) -> T: ...
