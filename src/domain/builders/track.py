from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4
from domain.builders.base import BaseBuilder
from domain.entities.track import Track
from domain.values.audio_url import AudioUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.title import Title


@dataclass(slots=True, init=False)
class TrackBuilder(BaseBuilder[Track]):
    _album_id: UUID
    _title: str
    _audio_url: str
    _duration: int

    def set_album(self, album_id: UUID | str) -> Self:
        if not isinstance(album_id, UUID):
            album_id = UUID(album_id)

        self._album_id = album_id
        return self

    def set_title(self, title: str) -> Self:
        self._title = title
        return self

    def set_audio(self, audio_url: str) -> Self:
        self._audio_url = audio_url
        return self

    def set_duration(self, duration: int) -> Self:
        self._duration = duration
        return self

    def build(self) -> Track:
        return Track(
            album_id=self._album_id,
            title=Title(self._title),
            audio_url=AudioUrl(self._audio_url),
            duration=Duration(self._duration),
            listens=Listens(0),
        )
