from dataclasses import dataclass, field
from uuid import UUID

from domain.models.entities.base import BaseEntity
from domain.models.entities.track import TrackItem
from domain.models.values.cover_url import CoverUrl
from domain.models.values.description import Description
from domain.models.values.title import Title


@dataclass(eq=False, slots=True, kw_only=True)
class Playlist(BaseEntity):
    user_id: UUID
    title: Title
    cover_url: CoverUrl
    description: Description = field(default=Description(None))

    def edit_title(self, title: str) -> None:
        self.title = Title(title)

    def edit_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)

    def edit_description(self, description: str) -> None:
        self.description = Description(description)

    def clear_description(self) -> None:
        self.description = Description(None)


@dataclass(eq=False, slots=True, kw_only=True)
class PlaylistInfo(Playlist):
    tracks: tuple[TrackItem] = field(default_factory=tuple)
