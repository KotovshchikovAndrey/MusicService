from typing import Protocol

from domain.entities.artist import Artist


class ArtistRepository(Protocol):
    async def get_by_oid(self, artist_oid: str) -> Artist | None: ...

    async def filter_by_oids(self, *artist_oids: str) -> list[Artist]: ...

    async def upsert(self, artist: Artist) -> None: ...
