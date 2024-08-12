from typing import Iterable, Literal, Protocol

from domain.entities.track import ChartedTrack, Track


class TrackRepository(Protocol):
    async def get_by_oid(self, track_oid: str) -> Track | None: ...

    async def get_top_chart_for_period(
        self, period: Literal["all_time", "day"], limit: int
    ) -> list[ChartedTrack]: ...

    async def upsert(self, track: Track) -> None: ...

    async def set_artists(self, track_oid: str, artist_oids: Iterable[str]) -> None: ...

    async def increment_listens(self, track_oid: str) -> None: ...
