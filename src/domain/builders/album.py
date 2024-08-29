from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from domain.builders.base import BaseBuilder
from domain.entities.album import Album
from domain.values.cover_url import CoverUrl
from domain.values.title import Title


@dataclass(slots=True, init=False)
class AlbumBuilder(BaseBuilder[Album]):
    _title: str
    _cover_url: str

    def set_title(self, title: str) -> Self:
        self._title = title
        return self

    def set_cover(self, cover_url: str) -> Self:
        self._cover_url = cover_url
        return self

    def build(self) -> Album:
        return Album(
            title=Title(self._title),
            cover_url=CoverUrl(self._cover_url),
            created_at=datetime.now(UTC),
        )
