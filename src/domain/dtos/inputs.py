from dataclasses import dataclass, field
from typing import Iterable

from domain.common.exceptions import BadRequestException
from domain.dtos.mixins import LimitMixin, OidMixin, PageMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class GetChartDto(LimitMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class GetNewReleasesDto(LimitMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class GetArtistsDto(PageMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateAlbumDto:
    title: str
    cover_filename: str


@dataclass(frozen=True, kw_only=True, slots=True)
class RegisterArtistDto(OidMixin):
    nickname: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UploadTrackDto:
    title: str
    duration: int
    album_oid: str
    audio_filename: str
    artist_oids: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.artist_oids:
            raise BadRequestException("Not specified 'artist_oids'")


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateArtistDto(OidMixin):
    nickname: str | None = field(default=None)
    avatar_url: str | None = field(default=None)


@dataclass(frozen=True, kw_only=True, slots=True)
class ListenTrackDto(OidMixin):
    start_byte: int = field(default=0)
    end_byte: int | None = field(default=None)
