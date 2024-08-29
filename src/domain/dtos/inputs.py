from dataclasses import dataclass, field
from uuid import UUID

from domain.common.exceptions import BadRequestException
from domain.dtos.mixins import LimitMixin, OidMixin, PageMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class GetChartDto(LimitMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class GetNewReleasesDto(LimitMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class GetArtistsDto(PageMixin): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class RegisterCreatedArtistDto(OidMixin):
    nickname: str
    avatar_download_url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UploadAlbumDto:
    title: str
    cover_download_url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UploadTrackDto:
    title: str
    duration: int
    audio_download_url: str
    artist_ids: set[UUID] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.artist_ids:
            raise BadRequestException("Not specified 'artist_ids'")


@dataclass(frozen=True, kw_only=True, slots=True)
class UploadReviewedAlbumDto:
    album: UploadAlbumDto
    tracks: tuple[UploadTrackDto]


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateArtistDto(OidMixin):
    nickname: str | None = field(default=None)
    avatar_url: str | None = field(default=None)


@dataclass(frozen=True, kw_only=True, slots=True)
class ListenTrackDto(OidMixin):
    start_byte: int = field(default=0)
    end_byte: int | None = field(default=None)
