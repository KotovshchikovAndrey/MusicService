from dataclasses import dataclass
from typing import Self
from uuid import UUID

from domain.builders.base import BaseBuilder
from domain.entities.artist import Artist
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname


@dataclass(slots=True, init=False)
class ArtistBuilder(BaseBuilder[Artist]):
    _user_id: UUID
    _nickname: str
    _avatar_url: str

    def set_user(self, user_id: UUID) -> Self:
        self._user_id = user_id
        return self

    def set_nickname(self, nickname: str) -> Self:
        self._nickname = nickname
        return self

    def set_avatar(self, avatar_url: str) -> Self:
        self._avatar_url = avatar_url
        return self

    def build(self) -> Artist:
        return Artist(
            id=self._user_id,
            nickname=Nickname(self._nickname),
            avatar_url=AvatarUrl(self._avatar_url),
        )
