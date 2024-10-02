from typing import Annotated

from pydantic import Field

from domain.models.entities.artist import Artist
from domain.ports.driving.base import BaseDTO, Pagination
from domain.usecases.base import BaseUseCase


class GetArtistsDTO(BaseDTO):
    page: Annotated[int, Field(default=1, gt=0)]


class PaginatedArtists(Pagination):
    artists: Annotated[list[Artist], Field(default_factory=list)]


class GetArtistsUseCase(BaseUseCase[GetArtistsDTO, PaginatedArtists]): ...
