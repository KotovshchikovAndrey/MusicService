import typing as tp

from domain.entities.album import Album


class AlbumRepository(tp.Protocol):
    async def get_new(self, limit: int, offset: int) -> list[Album]: ...

    async def get_one(self, album_oid: str) -> Album | None: ...

    async def save(self, album: Album) -> None: ...
