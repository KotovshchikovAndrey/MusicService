from dataclasses import dataclass
from uuid import UUID

from domain.entities.artist import Artist
from domain.factories.base import EntityFactory
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistFactory(EntityFactory[Artist]):
    user_id: UUID
    nickname: str
    avatar_url: str

    def create(self) -> Artist:
        return Artist(
            id=self.user_id,
            nickname=Nickname(self.nickname),
            avatar_url=AvatarUrl(self.avatar_url),
        )
