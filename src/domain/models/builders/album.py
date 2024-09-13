from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self

from domain.models.builders.base import BaseBuilder
from domain.models.entities.album import Album
from domain.models.values.cover_url import CoverUrl
from domain.models.values.title import Title


@dataclass(frozen=True, slots=True)
class AlbumBuilder(BaseBuilder[Album]):
    _album: Album = field(init=False, default_factory=Album)

    def set_title(self, title: str) -> Self:
        self._album.title = Title(title)
        return self

    def set_cover(self, cover_url: str) -> Self:
        self._album.cover_url = CoverUrl(cover_url)
        return self

    def build(self) -> Album:
        return self._album
