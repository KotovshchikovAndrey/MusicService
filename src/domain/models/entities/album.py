from dataclasses import dataclass, field
from datetime import UTC, datetime

from domain.models.entities.artist import BaseArtist
from domain.models.entities.base import BaseEntity
from domain.models.entities.track import TrackItem
from domain.models.values.cover_url import CoverUrl
from domain.models.values.title import Title


@dataclass(eq=False, slots=True, kw_only=True)
class Album(BaseEntity):
    title: Title
    cover_url: CoverUrl
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def edit_title(self, title: str) -> None:
        self.title = Title(title)

    def edit_cover(self, url: str) -> None:
        self.cover_url = CoverUrl(url)


@dataclass(eq=False, slots=True, kw_only=True)
class AlbumInfo(Album):
    tracks: tuple[TrackItem] = field(default_factory=tuple)

    def get_all_artists(self) -> set[BaseArtist]:
        artists = set()
        for track in self.tracks:
            artists.update(track.artists)

        return artists
