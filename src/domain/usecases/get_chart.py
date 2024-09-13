from typing import Iterable

from domain.models.entities.track import ChartedTrack
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.getting_chart import GetChartDto, GetChartUseCase


class GetChartUseCaseImpl(GetChartUseCase):
    _uow: UnitOfWork

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: GetChartDto) -> Iterable[ChartedTrack]:
        async with self._uow as uow:
            tracks = await uow.tracks.get_top_chart_for_period(
                period="day",
                limit=data.limit,
            )

            return tracks
