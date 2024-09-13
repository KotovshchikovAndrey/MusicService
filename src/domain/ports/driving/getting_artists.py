from dataclasses import dataclass, field
from typing import Iterable

from domain.models.entities.artist import Artist
from domain.ports.driving.base import PaginationMixin
from domain.usecases.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class GetArtistsDto:
    page: int = field(default=1)


@dataclass(frozen=True, kw_only=True, slots=True)
class PaginatedArtists(PaginationMixin):
    artists: Iterable[Artist] = field(default_factory=tuple)


class GetArtistsUseCase(BaseUseCase[GetArtistsDto, PaginatedArtists]): ...
