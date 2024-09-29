from typing import Iterable
from uuid import UUID

from domain.models.entities.artist import Artist
from domain.ports.driven.database.artist_repository import ArtistRepository


class ArtistMemcachedCaching(ArtistRepository):
    _repository: ArtistRepository

    def __init__(self, repository: ArtistRepository) -> None:
        self._repository = repository

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        raise NotImplementedError

    async def get_list(self, limit: int, offset: int) -> list[Artist]:
        raise NotImplementedError

    async def get_total_count(self) -> int:
        raise NotImplementedError

    async def filter_by_ids(self, artist_ids: Iterable[UUID]) -> list[Artist]:
        raise NotImplementedError

    async def save(self, artist: Artist) -> None:
        raise NotImplementedError
