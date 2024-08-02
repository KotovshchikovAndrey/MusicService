from typing import Protocol
from domain.entities.album import Album


class AlbumRepository(Protocol):
    async def get_new_releases(self, limit: int, offset: int) -> list[Album]: ...

    async def get_by_oid(
        self, album_oid: str, fetch_tracks: bool = False
    ) -> Album | None: ...

    async def upsert(self, album: Album) -> None: ...
