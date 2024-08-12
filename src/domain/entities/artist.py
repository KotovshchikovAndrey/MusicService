from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname


@dataclass(eq=False, kw_only=True, slots=True)
class ArtistLink(BaseEntity):
    nickname: Nickname


@dataclass(eq=False, kw_only=True, slots=True)
class Artist(ArtistLink):
    avatar_url: AvatarUrl

    def change_nickname(self, nickname: str) -> None:
        self.nickname = Nickname(nickname)

    def change_avatar(self, url: str) -> None:
        self.avatar_url = AvatarUrl(url)
