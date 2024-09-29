from uuid import UUID

from domain.models.entities.album import Album, AlbumInfo
from domain.ports.driven.database.album_repository import AlbumRepository


class AlbumRedisCaching(AlbumRepository):
    _repository: AlbumRepository

    def __init__(self, repository: AlbumRepository) -> None:
        self._repository = repository

    async def get_new_releases(self, limit: int) -> list[AlbumInfo]:
        raise NotImplementedError

    async def get_by_id(self, album_id: UUID) -> Album | None:
        raise NotImplementedError

    async def exists(self, album_id: UUID) -> bool:
        raise NotImplementedError

    async def save(self, album: Album) -> None:
        raise NotImplementedError
