from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID

import httpx

from domain.entities.base import BaseEntity
from domain.entities.track import Track


class ElasticSearch[TEntity: BaseEntity](ABC):
    _index_url: str

    def __init__(self, index_url: str) -> None:
        self._index_url = index_url

    def _parse_ids_from_response(
        self, response_data: dict, limit: int
    ) -> Iterable[UUID]:
        hits = response_data["hits"]["hits"]
        if limit >= len(hits):
            return [UUID(hit["_id"]) for hit in hits]

        ids = []
        for index in range(limit):
            ids.append(UUID(hits[index]["_id"]))

        return ids

    @abstractmethod
    async def upsert_index(self, entity: TEntity) -> None: ...

    @abstractmethod
    async def search(self, query: str, limit: int) -> Iterable[UUID]: ...


class TrackElasticSearch(ElasticSearch[Track]):
    async def upsert_index(self, entity: Track) -> None:
        async with httpx.AsyncClient(base_url=self._index_url) as client:
            data = {
                "id": entity.id.hex,
                "title": entity.title.value,
            }

            await client.post(url=f"/_doc/{entity.id.hex}", json=data)

    async def search(self, query: str, limit: int) -> Iterable[UUID]:
        async with httpx.AsyncClient(base_url=self._index_url) as client:
            data = {
                "_source": False,
                "query": {
                    "match": {
                        "title": query,
                    },
                },
            }

            response = await client.post(url=f"/_search", json=data)
            return self._parse_ids_from_response(
                response_data=dict(response.json()),
                limit=limit,
            )
