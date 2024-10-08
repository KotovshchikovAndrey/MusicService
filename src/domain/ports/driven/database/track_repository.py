from typing import Iterable, Literal, Protocol
from uuid import UUID

from domain.models.entities.track import PopularTrack, Track, TrackItem


class TrackRepository(Protocol):
    async def get_by_id(self, track_id: UUID) -> Track | None: ...

    async def get_most_popular_for_period(
        self, period: Literal["all_time", "day"], limit: int
    ) -> list[PopularTrack]: ...

    async def get_items_by_ids(
        self, track_ids: Iterable[UUID]
    ) -> Iterable[TrackItem]: ...

    async def save(self, track: Track) -> None: ...

    async def save_all(self, tracks: Iterable[Track]) -> None: ...

    async def specify_artists(
        self, track_id: UUID, artist_ids: Iterable[UUID]
    ) -> None: ...

    async def check_user_is_listener(self, track_id: UUID, user_id: UUID) -> bool: ...

    async def set_last_listened_date(self, track_id: UUID, user_id: UUID) -> None: ...
