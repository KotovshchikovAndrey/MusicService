from typing import Protocol

from domain.entities.base import BaseEntity


class EntityFactory[TEntity: BaseEntity](Protocol):
    def create(self) -> TEntity: ...
