from dataclasses import dataclass
from uuid import UUID

from domain.entities.playlist import Playlist
from domain.factories.base import EntityFactory
from domain.values.cover_url import CoverUrl
from domain.values.description import Description
from domain.values.title import Title


@dataclass(frozen=True, kw_only=True, slots=True)
class PlaylistFactory(EntityFactory[Playlist]):
    user_id: UUID
    title: str
    cover_url: str
    description: str | None

    def create(self) -> Playlist:
        return Playlist(
            user_id=self.user_id,
            title=Title(self.title),
            cover_url=CoverUrl(self.cover_url),
            description=Description(self.description),
        )
