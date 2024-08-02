from typing import Self, Type
from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.nickname import Nickname


@dataclass(eq=False, kw_only=True, slots=True)
class Artist(BaseEntity):
    nickname: Nickname
    # avatar_url: ...

    @classmethod
    def create(
        cls: Type["Artist"],
        nickname: str,
        # avatar_url: str,
    ) -> Self:
        return cls(
            nickname=Nickname(nickname),
            # avatar_url=
        )

    def change_nickname(self, nickname: str) -> None:
        self.nickname = Nickname(nickname)
