import typing as tp
from dataclasses import dataclass, field

from domain.dtos.artist import ArtistDto
from domain.dtos.base import OidMixin, PaginationMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class GetChartDto(PaginationMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class TrackDto(OidMixin):
    title: str
    audio_url: str
    duration: int
    artists: list[ArtistDto] = field(default_factory=list)


@dataclass(frozen=True, kw_only=True, slots=True)
class PlayTrackDto(OidMixin): ...
