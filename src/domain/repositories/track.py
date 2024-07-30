import typing as tp
from domain.entities.track import Track


class TrackRepository(tp.Protocol):
    async def get_one(self, track_oid: str) -> Track | None: ...

    async def get_popular(self, limit: int, offset: int) -> list[Track]: ...

    async def save(self, track: Track) -> None: ...
