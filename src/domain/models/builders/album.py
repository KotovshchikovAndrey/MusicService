from dataclasses import dataclass
from typing import Self

from domain.models.builders.base import BaseBuilder
from domain.models.entities.album import Album
from domain.models.values.cover_url import CoverUrl
from domain.models.values.title import Title


@dataclass(eq=False, init=False, slots=True)
class AlbumBuilder(BaseBuilder[Album]):
    _title: Title
    _cover_url: CoverUrl

    def set_title(self, title: str) -> Self:
        self._title = Title(title)
        return self

    def set_cover(self, cover_url: str) -> Self:
        self._cover_url = CoverUrl(cover_url)
        return self

    def build(self) -> Album:
        return Album(
            title=self._title,
            cover_url=self._cover_url,
        )
