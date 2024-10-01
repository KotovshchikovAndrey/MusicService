from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, HttpUrl, AfterValidator

from domain.ports.driving.base import BaseDTO, BaseUseCase


class AlbumMetaData(BaseDTO):
    title: str
    cover_url: Annotated[HttpUrl, AfterValidator(func=lambda url: str(url))]


class TrackMetaData(BaseDTO):
    title: str
    duration: int
    audio_url: Annotated[HttpUrl, AfterValidator(func=lambda url: str(url))]
    artist_ids: Annotated[set[UUID], Field(min_length=1, max_length=15)]


class UploadAlbumDTO(BaseDTO):
    album: AlbumMetaData
    tracks: Annotated[list[TrackMetaData], Field(min_length=1, max_length=100)]


class UploadAlbumUseCase(BaseUseCase[UploadAlbumDTO, UUID]): ...
