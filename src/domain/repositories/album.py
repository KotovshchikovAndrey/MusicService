from typing import Protocol
from uuid import UUID

from domain.entities.album import Album, AlbumInfo


class AlbumRepository(Protocol):
    async def get_new_releases(self, limit: int) -> list[AlbumInfo]: ...

    async def get_by_id(self, album_id: UUID) -> Album | None: ...

    async def check_exists(self, album_id: UUID) -> bool: ...

    async def upsert(self, album: Album) -> None: ...
