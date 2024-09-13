from dataclasses import dataclass, field
from uuid import UUID

from domain.models.entities.artist import Artist
from domain.ports.driving.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateArtistDto:
    artist_id: UUID
    nickname: str | None = field(default=None)
    avatar_url: str | None = field(default=None)


class UpdateArtistUseCase(BaseUseCase[UpdateArtistDto, Artist]): ...
