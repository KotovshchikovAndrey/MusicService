from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.entities.track import TrackItem
from domain.values.cover_url import CoverUrl
from domain.values.description import Description
from domain.values.oid import OID
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Playlist(BaseEntity):
    user_oid: OID
    title: Title
    cover_url: CoverUrl
    description: Description = field(default=Description(None))

    def change_title(self, title: str) -> None:
        self.title = Title(title)

    def change_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)

    def change_description(self, description: str) -> None:
        self.description = Description(description)

    def clear_description(self) -> None:
        self.description = Description(None)


@dataclass(eq=False, kw_only=True, slots=True)
class PlaylistInfo(Playlist):
    tracks: tuple[TrackItem] = field(default_factory=tuple)
