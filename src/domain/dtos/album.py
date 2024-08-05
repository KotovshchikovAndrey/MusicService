from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable

from domain.dtos.base import LimitMixin, OidMixin
from domain.dtos.track import TrackDto


@dataclass(frozen=True, kw_only=True, slots=True)
class GetNewReleasesDto(LimitMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class AlbumDto(OidMixin):
    title: str
    cover_url: str
    created_at: datetime
    tracks: Iterable[TrackDto] = field(default_factory=list)


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateAlbumDto:
    title: str
    cover_filename: str
