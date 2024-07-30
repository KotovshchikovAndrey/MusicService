from dataclasses import dataclass, field

from domain.entities.artist import Artist
from domain.entities.base import BaseEntity

from domain.values.audio_url import AudioUrl
from domain.values.duration import Duration
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Track(BaseEntity):
    title: Title
    audio_url: AudioUrl
    duration: Duration
    artists: set[Artist] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.artists:
            raise ValueError("No artist is specified")

    def set_title(self, title: str, my_oid: str) -> None:
        if not self._is_artist(my_oid):
            raise ValueError("Permission denied")

        self.title = Title(title)

    def _is_artist(self, oid: str) -> bool:
        for artist in self.artists:
            if artist.oid == oid:
                return True

        return False
