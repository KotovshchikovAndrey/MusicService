from typing import Self, Type
from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.entities.track import Track

from domain.values.cover_url import CoverUrl
from domain.values.description import Description
from domain.values.oid import OID
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Playlist(BaseEntity):
    user_oid: UUID
    title: Title
    cover_url: CoverUrl
    description: Description = field(default=Description(None))
    tracks: tuple[Track] = field(default_factory=tuple)

    @classmethod
    def create(
        cls: Type["Playlist"],
        user_oid: str,
        title: str = "Untitled",
        cover_url: str = "/default_playlist_cover.png",
        description: str | None = None,
    ) -> Self:
        return cls(
            user_oid=OID(user_oid),
            title=Title(title),
            cover_url=CoverUrl(cover_url),
            description=Description(description),
        )

    def change_title(self, title: str) -> None:
        self.title = Title(title)

    def change_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)

    def change_description(self, description: str) -> None:
        self.description = Description(description)

    def clear_description(self) -> None:
        self.description = Description(None)
