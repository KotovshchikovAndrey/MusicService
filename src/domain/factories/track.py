from dataclasses import dataclass

from domain.entities.track import Track
from domain.factories.base import EntityFactory
from domain.values.audio_url import AudioUrl
from domain.values.duration import Duration
from domain.values.listens import Listens
from domain.values.oid import OID
from domain.values.title import Title


@dataclass(frozen=True, kw_only=True, slots=True)
class TrackFactory(EntityFactory[Track]):
    album_oid: str
    title: str
    audio_url: str
    duration: int

    def create(self) -> Track:
        return Track(
            album_oid=OID(self.album_oid),
            title=Title(self.title),
            audio_url=AudioUrl(self.audio_url),
            duration=Duration(self.duration),
            listens=Listens(0),
        )
