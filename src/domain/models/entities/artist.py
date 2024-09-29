from dataclasses import dataclass

from domain.models.entities.base import BaseEntity
from domain.models.values.avatar_url import AvatarUrl
from domain.models.values.nickname import Nickname


@dataclass(eq=False, slots=True, kw_only=True)
class BaseArtist(BaseEntity):
    nickname: Nickname


@dataclass(eq=False, slots=True, kw_only=True)
class Artist(BaseArtist):
    avatar_url: AvatarUrl

    def edit_nickname(self, nickname: str) -> None:
        self.nickname = Nickname(nickname)

    def edit_avatar(self, url: str) -> None:
        self.avatar_url = AvatarUrl(url)
