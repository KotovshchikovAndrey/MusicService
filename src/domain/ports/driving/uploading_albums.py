from dataclasses import dataclass
from uuid import UUID

from domain.exceptions.album import InvalidAlbumUploadingData
from domain.ports.driving.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class AlbumMetaData:
    title: str
    cover_download_url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class TrackMetaData:
    title: str
    duration: int
    audio_download_url: str
    artist_ids: set[UUID]

    def __post_init__(self) -> None:
        if not self.artist_ids:
            raise InvalidAlbumUploadingData(reason="Artist_ids not specified")


@dataclass(frozen=True, kw_only=True, slots=True)
class UploadAlbumDto:
    album: AlbumMetaData
    tracks: tuple[TrackMetaData]


class UploadAlbumUseCase(BaseUseCase[UploadAlbumDto, None]): ...
