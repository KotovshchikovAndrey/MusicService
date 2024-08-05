from dataclasses import dataclass, field

from domain.dtos.base import OidMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class RegisterArtistDto(OidMixin):
    nickname: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateArtistDto(OidMixin):
    nickname: str | None = field(default=None)
    avatar_url: str | None = field(default=None)


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistDto(RegisterArtistDto):
    avatar_url: str
