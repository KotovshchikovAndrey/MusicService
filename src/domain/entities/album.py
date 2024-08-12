from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.artist import ArtistLink
from domain.entities.base import BaseEntity
from domain.entities.track import TrackItem
from domain.values.cover_url import CoverUrl
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Album(BaseEntity):
    title: Title
    cover_url: CoverUrl
    created_at: datetime

    def change_title(self, title: str) -> None:
        self.title = Title(title)

    def change_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)


@dataclass(eq=False, kw_only=True, slots=True)
class AlbumInfo(Album):
    tracks: tuple[TrackItem] = field(default_factory=tuple)

    def get_artists(self) -> set[ArtistLink]:
        artists = set()
        for track in self.tracks:
            artists.update(track.artists)

        return artists
