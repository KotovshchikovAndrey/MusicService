from dataclasses import dataclass, field
from uuid import UUID

from domain.models.entities.base import BaseEntity
from domain.models.entities.track import TrackItem
from domain.models.values.cover_url import CoverUrl
from domain.models.values.description import Description
from domain.models.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Playlist(BaseEntity):
    user_id: UUID = field(init=False)
    title: Title = field(init=False)
    cover_url: CoverUrl = field(init=False)
    description: Description = field(init=False, default=Description(None))

    def edit_title(self, title: str) -> None:
        self.title = Title(title)

    def edit_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)

    def edit_description(self, description: str) -> None:
        self.description = Description(description)

    def clear_description(self) -> None:
        self.description = Description(None)


@dataclass(eq=False, kw_only=True, slots=True)
class PlaylistInfo(Playlist):
    tracks: tuple[TrackItem] = field(init=False, default_factory=tuple)
