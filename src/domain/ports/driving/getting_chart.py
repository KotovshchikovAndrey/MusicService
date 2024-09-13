from dataclasses import dataclass, field
from typing import Iterable
from uuid import UUID

from domain.models.entities.track import ChartedTrack
from domain.ports.driving.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class GetChartDto:
    limit: int = field(default=100)


class GetChartUseCase(BaseUseCase[GetChartDto, Iterable[ChartedTrack]]): ...
