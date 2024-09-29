from dataclasses import dataclass
from typing import Self
from uuid import UUID

from domain.models.builders.base import BaseBuilder
from domain.models.entities.artist import Artist
from domain.models.values.avatar_url import AvatarUrl
from domain.models.values.nickname import Nickname


@dataclass(eq=False, init=False, slots=True)
class ArtistBuilder(BaseBuilder[Artist]):
    _id: UUID
    _nickname: Nickname
    _avatar_url: AvatarUrl

    def set_id(self, user_id: UUID) -> Self:
        self._id = user_id
        return self

    def set_nickname(self, nickname: str) -> Self:
        self._nickname = Nickname(nickname)
        return self

    def set_avatar(self, avatar_url: str) -> Self:
        self._avatar_url = AvatarUrl(avatar_url)
        return self

    def build(self) -> Artist:
        return Artist(
            id=self._id,
            nickname=self._nickname,
            avatar_url=self._avatar_url,
        )
