from domain.dtos.track import GetChartDto, TrackDto
from domain.mappers.track import map_to_track_dto
from domain.usecases.base import BaseUseCase
from domain.utils.uow import UnitOfWork


class GetChartUseCase(BaseUseCase[GetChartDto, list[TrackDto]]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetChartDto) -> list[TrackDto]:
        async with self._uow as uow:
            tracks = await uow.tracks.get_top_for_day(limit=data.limit)
            return [map_to_track_dto(track) for track in tracks]
