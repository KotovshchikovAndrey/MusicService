from typing import Iterable
from uuid import UUID


def parse_ids_from_elastic_response(response_data: dict, limit: int) -> Iterable[UUID]:
    hits = response_data["hits"]["hits"]
    if limit >= len(hits):
        return [UUID(hit["_id"]) for hit in hits]

    ids = []
    for index in range(limit):
        ids.append(UUID(hits[index]["_id"]))

    return ids


def build_index_url(address: str, index: str, use_ssl: bool) -> str:
    protocol = "http" if not use_ssl else "https"
    return f"{protocol}://{address}/{index}"
