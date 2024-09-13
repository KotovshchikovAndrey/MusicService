from dataclasses import dataclass, field
from uuid import UUID

from domain.models.entities.artist import BaseArtist
from domain.models.entities.base import BaseEntity
from domain.models.values.audio_url import AudioUrl
from domain.models.values.cover_url import CoverUrl
from domain.models.values.duration import Duration
from domain.models.values.listens import Listens
from domain.models.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Track(BaseEntity):
    album_id: UUID = field(init=False)
    title: Title = field(init=False)
    audio_url: AudioUrl = field(init=False)
    duration: Duration = field(init=False)
    listens: Listens = field(init=False, default=Listens(0))

    def edit_title(self, title: str) -> None:
        self.title = Title(title)


@dataclass(eq=False, kw_only=True, slots=True)
class TrackItem(Track):
    artists: tuple[BaseArtist] = field(init=False, default_factory=tuple)


@dataclass(eq=False, kw_only=True, slots=True)
class ChartedTrack(TrackItem):
    cover_url: CoverUrl = field(init=False)
