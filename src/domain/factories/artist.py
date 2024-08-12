from dataclasses import dataclass

from domain.entities.artist import Artist
from domain.factories.base import EntityFactory
from domain.values.avatar_url import AvatarUrl
from domain.values.nickname import Nickname
from domain.values.oid import OID


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistFactory(EntityFactory[Artist]):
    user_oid: str
    nickname: str
    avatar_url: str

    def create(self) -> Artist:
        return Artist(
            oid=OID(self.user_oid),
            nickname=Nickname(self.nickname),
            avatar_url=AvatarUrl(self.avatar_url),
        )
