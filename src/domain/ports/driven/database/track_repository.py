from typing import Iterable, Literal, Protocol
from uuid import UUID

from domain.models.entities.track import ChartedTrack, Track


class TrackRepository(Protocol):
    async def get_by_id(self, track_id: UUID) -> Track | None: ...

    async def get_top_chart_for_period(
        self, period: Literal["all_time", "day"], limit: int
    ) -> list[ChartedTrack]: ...

    async def save(self, track: Track) -> None: ...

    async def save_all(self, tracks: Iterable[Track]) -> None: ...

    async def set_artists(self, track_id: UUID, artist_ids: Iterable[UUID]) -> None: ...

    async def increment_listens(self, track_id: UUID) -> None: ...
