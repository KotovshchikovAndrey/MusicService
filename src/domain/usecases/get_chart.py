from domain.common.mappers import map_to_charted_track_dto
from domain.dtos.inputs import GetChartDto
from domain.dtos.outputs import ChartedTrackDto
from domain.usecases.base import BaseUseCase
from domain.utils.uow import UnitOfWork


class GetChartUseCase(BaseUseCase[GetChartDto, list[ChartedTrackDto]]):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetChartDto) -> list[ChartedTrackDto]:
        async with self._uow as uow:
            tracks = await uow.tracks.get_top_chart_for_period(
                period="day",
                limit=data.limit,
            )

            return [map_to_charted_track_dto(track) for track in tracks]
