from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.entities.track import Track

from domain.values.cover_url import CoverUrl
from domain.values.description import Description
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Playlist(BaseEntity):
    user_id: str
    title: Title
    cover_url: CoverUrl
    description: Description = field(default=Description(None))
    tracks: set[Track] = field(default_factory=set)

    def set_title(self, title: str) -> None:
        self.title = Title(title)

    def set_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)

    def set_description(self, description: str) -> None:
        self.description = Description(description)

    def clear_description(self) -> None:
        self.description = Description(None)

    def add_track(self, track: Track) -> None:
        self.tracks.add(track)
