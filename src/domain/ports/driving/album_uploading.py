from typing import Annotated
from uuid import UUID

from pydantic import Field

from domain.ports.driving.base import BaseDTO, BaseUseCase


class AlbumMetaData(BaseDTO):
    title: str
    cover_download_url: str


class TrackMetaData(BaseDTO):
    title: str
    duration: int
    audio_download_url: str
    artist_ids: Annotated[set[UUID], Field(min_length=1, max_length=15)]


class UploadAlbumDTO(BaseDTO):
    album: AlbumMetaData
    tracks: Annotated[list[TrackMetaData], Field(min_length=1, max_length=100)]


class UploadAlbumUseCase(BaseUseCase[UploadAlbumDTO, UUID]): ...
