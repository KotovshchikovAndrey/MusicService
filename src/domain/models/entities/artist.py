from dataclasses import dataclass, field

from domain.models.entities.base import BaseEntity
from domain.models.values.avatar_url import AvatarUrl
from domain.models.values.nickname import Nickname


@dataclass(eq=False, kw_only=True, slots=True)
class BaseArtist(BaseEntity):
    nickname: Nickname = field(init=False)


@dataclass(eq=False, kw_only=True, slots=True)
class Artist(BaseArtist):
    avatar_url: AvatarUrl = field(init=False)

    def edit_nickname(self, nickname: str) -> None:
        self.nickname = Nickname(nickname)

    def edit_avatar(self, url: str) -> None:
        self.avatar_url = AvatarUrl(url)
