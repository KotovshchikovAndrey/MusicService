from domain.dtos.track import GetChartDto, TrackDto
from domain.mappers.track import map_to_track_dto
from domain.utils.uow import UnitOfWork
from domain.usecases.base import BaseUseCase


class GetChartUseCase(BaseUseCase[GetChartDto, list[TrackDto]]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetChartDto) -> list[TrackDto]:
        async with self._uow as uow:
            tracks = await uow.tracks.get_popular(limit=data.limit, offset=data.offset)
            return [map_to_track_dto(track) for track in tracks]
