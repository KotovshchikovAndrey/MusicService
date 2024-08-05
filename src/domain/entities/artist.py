from dataclasses import dataclass
from typing import Self, Type

from domain.entities.base import BaseEntity
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname


@dataclass(eq=False, kw_only=True, slots=True)
class Artist(BaseEntity):
    nickname: Nickname
    avatar_url: AvatarUrl

    @classmethod
    def create(
        cls: Type["Artist"],
        oid: str,
        nickname: str,
        avatar_url: str,
    ) -> Self:
        return cls(
            nickname=Nickname(nickname),
            avatar_url=AvatarUrl(avatar_url),
        )

    def change_nickname(self, nickname: str) -> None:
        self.nickname = Nickname(nickname)

    def change_avatar(self, url: str) -> None:
        self.avatar_url = AvatarUrl(url)
