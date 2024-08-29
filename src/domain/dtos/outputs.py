from dataclasses import dataclass, field
from typing import AsyncGenerator, Iterable

from domain.dtos.mixins import OidMixin, PaginationMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistLinkDto(OidMixin):
    nickname: str


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistDto(ArtistLinkDto):
    avatar_url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistListDto(PaginationMixin):
    artists: Iterable[ArtistDto] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True, slots=True)
class TrackItemDto(OidMixin):
    title: str
    audio_url: str
    duration: int
    artists: Iterable[ArtistLinkDto]


@dataclass(frozen=True, kw_only=True, slots=True)
class ChartedTrackDto(TrackItemDto):
    cover_url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class AlbumInfoDto(OidMixin):
    title: str
    cover_url: str
    created_at: str
    tracks: Iterable[TrackItemDto] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True, slots=True)
class AudioStreamDto:
    stream: AsyncGenerator[bytes, None]
    content_type: str
    content_length: str
    content_range: str
