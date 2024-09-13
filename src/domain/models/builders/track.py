from dataclasses import dataclass, field
from typing import Self
from uuid import UUID

from domain.models.builders.base import BaseBuilder
from domain.models.entities.track import Track
from domain.models.values.audio_url import AudioUrl
from domain.models.values.duration import Duration
from domain.models.values.title import Title


@dataclass(frozen=True, slots=True)
class TrackBuilder(BaseBuilder[Track]):
    _track: Track = field(init=False, default_factory=Track)

    def set_album(self, album_id: UUID) -> Self:
        self._track.album_id = album_id
        return self

    def set_title(self, title: str) -> Self:
        self._track.title = Title(title)
        return self

    def set_audio(self, audio_url: str) -> Self:
        self._track.audio_url = AudioUrl(audio_url)
        return self

    def set_duration(self, duration: int) -> Self:
        self._track.duration = Duration(duration)
        return self

    def build(self) -> Track:
        return self._track
