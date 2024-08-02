from typing import AsyncGenerator
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
class ListenTrackDto(OidMixin):
    start_byte: int = field(default=0)
    end_byte: int | None = field(default=None)


@dataclass(kw_only=True, slots=True)
class AudioStreamDto:
    stream: AsyncGenerator[bytes, None]
    content_type: str
    content_length: str
    content_range: str
