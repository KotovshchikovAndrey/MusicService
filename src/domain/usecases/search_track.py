from domain.models.entities.track import TrackItem
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driven.search_engine import TrackSearchEngine
from domain.ports.driving.track_search import SearchTrackDTO, SearchTrackUseCase


class SearchTrackUseCaseImpl(SearchTrackUseCase):
    _uow: UnitOfWork
    _search_engine: TrackSearchEngine

    def __init__(self, uow: UnitOfWork, search_engine: TrackSearchEngine) -> None:
        self._uow = uow
        self._search_engine = search_engine

    async def execute(self, data: SearchTrackDTO) -> list[TrackItem]:
        track_ids = await self._search_engine.search(query=data.query, limit=data.limit)
        async with self._uow as uow:
            tracks = await uow.tracks.get_items_by_ids(track_ids)
            return tracks
