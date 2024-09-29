from typing import Annotated

from pydantic import Field

from domain.models.entities.track import PopularTrack
from domain.ports.driving.base import BaseDTO, BaseUseCase


class GetChartDTO(BaseDTO):
    limit: Annotated[int, Field(default=100, gt=0, le=100)]


class GetChartUseCase(BaseUseCase[GetChartDTO, list[PopularTrack]]): ...
