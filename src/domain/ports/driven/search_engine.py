from asyncio import Protocol
from typing import Iterable
from uuid import UUID

from domain.models.entities.base import BaseEntity
from domain.models.entities.track import Track


class SearchEngine[TEntity: BaseEntity](Protocol):
    async def search(self, query: str, limit: int) -> Iterable[UUID]: ...

    async def make_searchable(self, entity: TEntity) -> None: ...


class TrackSearchEngine(SearchEngine[Track]): ...
