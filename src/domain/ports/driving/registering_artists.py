from dataclasses import dataclass
from uuid import UUID

from domain.ports.driving.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class RegisterArtistDto:
    user_id: UUID
    nickname: str
    avatar_download_url: str


class RegisterArtistUseCase(BaseUseCase[RegisterArtistDto, None]): ...
