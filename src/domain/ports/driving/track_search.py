from typing import Annotated

from pydantic import Field

from domain.models.entities.track import TrackItem
from domain.ports.driving.base import BaseDTO, BaseUseCase


class SearchTrackDTO(BaseDTO):
    limit: Annotated[int, Field(default=5, gt=0, le=100)]
    query: Annotated[str, Field(min_length=1, max_length=50)]


class SearchTrackUseCase(BaseUseCase[SearchTrackDTO, list[TrackItem]]): ...
