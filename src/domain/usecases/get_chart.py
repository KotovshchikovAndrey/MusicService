from domain.models.entities.track import PopularTrack
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.chart_getting import GetChartDTO, GetChartUseCase


class GetChartUseCaseImpl(GetChartUseCase):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetChartDTO) -> list[PopularTrack]:
        async with self._uow as uow:
            tracks = await uow.tracks.get_most_popular_for_period(
                period="day",
                limit=data.limit,
            )

            return tracks
