from typing import Protocol

from domain.entities.album import Album, AlbumInfo


class AlbumRepository(Protocol):
    async def get_new_releases(self, limit: int) -> list[AlbumInfo]: ...

    async def get_by_oid(self, album_oid: str) -> Album | None: ...

    async def check_exists(self, album_oid: str) -> bool: ...

    async def upsert(self, album: Album) -> None: ...
