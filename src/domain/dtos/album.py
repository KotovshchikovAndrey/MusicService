import typing as tp

from dataclasses import dataclass, field
from datetime import datetime
from domain.dtos.base import OidMixin, PaginationDto
from domain.dtos.track import TrackDto


@dataclass(frozen=True, kw_only=True, slots=True)
class GetNewReleasesDto(PaginationDto): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class AlbumDto(OidMixin):
    title: str
    cover_url: str
    created_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class AlbumWithTracksDto(AlbumDto):
    tracks: list[TrackDto] = field(default_factory=list)
