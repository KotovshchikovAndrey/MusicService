from dataclasses import dataclass, field
from uuid import UUID

from domain.models.entities.artist import BaseArtist
from domain.models.entities.base import BaseEntity
from domain.models.values.audio_url import AudioUrl
from domain.models.values.cover_url import CoverUrl
from domain.models.values.duration import Duration
from domain.models.values.listens import Listens
from domain.models.values.title import Title


@dataclass(eq=False, slots=True, kw_only=True)
class Track(BaseEntity):
    album_id: UUID
    title: Title
    audio_url: AudioUrl
    duration: Duration

    def edit_title(self, title: str) -> None:
        self.title = Title(title)


@dataclass(eq=False, slots=True, kw_only=True)
class TrackItem(Track):
    artists: tuple[BaseArtist] = field(default_factory=tuple)


@dataclass(eq=False, slots=True, kw_only=True)
class PopularTrack(TrackItem):
    cover_url: CoverUrl
    listens: Listens = field(default=Listens(0))
