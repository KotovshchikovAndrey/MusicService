from dataclasses import dataclass, field
from typing import Self, Type

from domain.entities.artist import Artist
from domain.entities.base import BaseEntity

from domain.values.audio_url import AudioUrl
from domain.values.duration import Duration
from domain.values.oid import OID
from domain.values.title import Title


@dataclass(eq=False, kw_only=True, slots=True)
class Track(BaseEntity):
    album_oid: OID
    title: Title
    audio_url: AudioUrl
    duration: Duration
    artists: tuple[Artist] = field(default_factory=tuple)

    @classmethod
    def create(
        cls: Type["Track"],
        album_oid: str,
        title: str,
        audio_url: str,
        duration: int,
    ) -> Self:
        return cls(
            album_oid=OID(album_oid),
            title=Title(title),
            audio_url=AudioUrl(audio_url),
            duration=Duration(duration),
        )

    def change_title(self, title: str) -> None:
        self.title = Title(title)
