from typing import Iterable
from uuid import UUID

import httpx

from adapters.driven.elasticsearch import utils
from domain.models.entities.track import Track
from domain.ports.driven.search_engine import TrackSearchEngine


class TrackElasticSearch(TrackSearchEngine):
    _index_url: str

    def __init__(
        self,
        address: str,
        index: str,
        use_ssl: bool = False,
    ) -> None:
        self._index_url = utils.build_index_url(address, index, use_ssl)

    async def make_searchable(self, entity: Track) -> None:
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

            response = await client.post(url="/_search", json=data)
            return utils.parse_ids_from_elastic_response(
                response_data=dict(response.json()),
                limit=limit,
            )
