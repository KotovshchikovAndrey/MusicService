from typing import Iterable, Literal
from uuid import UUID

from domain.models.entities.track import PopularTrack, Track, TrackItem
from domain.ports.driven.database.track_repository import TrackRepository


class TrackMemcachedCaching(TrackRepository):
    _repository: TrackRepository

    def __init__(self, repository: TrackRepository) -> None:
        self._repository = repository

    async def get_by_id(self, track_id: UUID) -> Track | None:
        raise NotImplementedError

    async def get_most_popular_for_period(
        self, period: Literal["all_time"] | Literal["day"], limit: int
    ) -> list[PopularTrack]:
        raise NotImplementedError

    async def get_items_by_ids(self, track_ids: Iterable[UUID]) -> Iterable[TrackItem]:
        raise NotImplementedError

    async def save(self, track: Track) -> None:
        raise NotImplementedError

    async def save_all(self, tracks: Iterable[Track]) -> None:
        raise NotImplementedError

    async def set_artists(self, track_id: UUID, artist_ids: Iterable[UUID]) -> None:
        raise NotImplementedError

    async def check_user_is_listener(self, track_id: UUID, user_id: UUID) -> bool:
        raise NotImplementedError

    async def set_last_listened_date(self, track_id: UUID, user_id: UUID) -> None:
        raise NotImplementedError
