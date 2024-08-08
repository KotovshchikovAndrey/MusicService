from dataclasses import dataclass, field
from typing import AsyncGenerator, Iterable

from domain.dtos.artist import ArtistDto
from domain.dtos.base import LimitMixin, OidMixin
from domain.exceptions.bad_request import BadRequestException


@dataclass(frozen=True, kw_only=True, slots=True)
class GetChartDto(LimitMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class TrackDto(OidMixin):
    album_oid: str
    title: str
    audio_url: str
    duration: int
    cover_url: str
    artists: Iterable[ArtistDto] = field(default_factory=list)


@dataclass(frozen=True, kw_only=True, slots=True)
class ListenTrackDto(OidMixin):
    start_byte: int = field(default=0)
    end_byte: int | None = field(default=None)


@dataclass(frozen=True, kw_only=True, slots=True)
class AudioStreamDto:
    stream: AsyncGenerator[bytes, None]
    content_type: str
    content_length: str
    content_range: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UploadTrackDto:
    title: str
    duration: int
    album_oid: str
    audio_filename: str
    artist_oids: Iterable[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.artist_oids:
            raise BadRequestException("Not specified 'artist_oids'")
