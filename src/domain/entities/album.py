from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self, Type

from domain.entities.base import BaseEntity
from domain.entities.track import Track
from domain.values.cover_url import CoverUrl
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Album(BaseEntity):
    title: Title
    cover_url: CoverUrl
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    tracks: tuple[Track] = field(default_factory=tuple)

    @classmethod
    def create(
        cls: Type["Album"],
        title: str,
        cover_url: str,
    ) -> Self:
        return cls(
            title=Title(title),
            cover_url=CoverUrl(cover_url),
        )

    def change_title(self, title: str) -> None:
        self.title = Title(title)

    def change_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)
