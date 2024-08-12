from dataclasses import dataclass
from datetime import UTC, datetime

from domain.entities.album import Album
from domain.factories.base import EntityFactory
from domain.values.cover_url import CoverUrl
from domain.values.title import Title


@dataclass(frozen=True, kw_only=True, slots=True)
class AlbumFactory(EntityFactory[Album]):
    title: str
    cover_url: str

    def create(self) -> Album:
        return Album(
            title=Title(self.title),
            cover_url=CoverUrl(self.cover_url),
            created_at=datetime.now(UTC),
        )
