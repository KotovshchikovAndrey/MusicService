from dataclasses import dataclass, field
from typing import Self
from uuid import UUID

from domain.models.builders.base import BaseBuilder
from domain.models.entities.artist import Artist
from domain.models.values.avatar_url import AvatarUrl
from domain.models.values.nickname import Nickname


@dataclass(frozen=True, slots=True)
class ArtistBuilder(BaseBuilder[Artist]):
    _artist: Artist = field(init=False, default_factory=Artist)

    def set_user(self, user_id: UUID) -> Self:
        self._artist.id = user_id
        return self

    def set_nickname(self, nickname: str) -> Self:
        self._artist.nickname = Nickname(nickname)
        return self

    def set_avatar(self, avatar_url: str) -> Self:
        self._artist.avatar_url = AvatarUrl(avatar_url)
        return self

    def build(self) -> Artist:
        return self._artist
