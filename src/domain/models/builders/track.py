from dataclasses import dataclass
from typing import Self
from uuid import UUID

from domain.models.builders.base import BaseBuilder
from domain.models.entities.track import Track
from domain.models.values.audio_url import AudioUrl
from domain.models.values.duration import Duration
from domain.models.values.title import Title


@dataclass(eq=False, slots=True, init=False)
class TrackBuilder(BaseBuilder[Track]):
    _album_id: UUID
    _title: Title
    _audio_url: AudioUrl
    _duration: Duration

    def set_album(self, album_id: UUID) -> Self:
        self._album_id = album_id
        return self

    def set_title(self, title: str) -> Self:
        self._title = Title(title)
        return self

    def set_audio(self, audio_url: str) -> Self:
        self._audio_url = AudioUrl(audio_url)
        return self

    def set_duration(self, duration: int) -> Self:
        self._duration = Duration(duration)
        return self

    def build(self) -> Track:
        return Track(
            album_id=self._album_id,
            title=self._title,
            audio_url=self._audio_url,
            duration=self._duration,
        )
