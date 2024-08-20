from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.artist import ArtistLink
from domain.entities.base import BaseEntity
from domain.values.audio_url import AudioUrl
from domain.values.cover_url import CoverUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Track(BaseEntity):
    album_id: UUID
    title: Title
    audio_url: AudioUrl
    duration: Duration
    listens: Listens

    def change_title(self, title: str) -> None:
        self.title = Title(title)


@dataclass(eq=False, kw_only=True, slots=True)
class TrackItem(Track):
    artists: tuple[ArtistLink] = field(default_factory=tuple)


@dataclass(eq=False, kw_only=True, slots=True)
class ChartedTrack(TrackItem):
    cover_url: CoverUrl
