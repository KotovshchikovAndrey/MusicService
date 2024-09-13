from typing import Annotated, Iterable
from uuid import UUID

from pydantic import BaseModel, Field

from domain.ports.driving.registering_artists import RegisterArtistDto
from domain.ports.driving.uploading_albums import (
    AlbumMetaData,
    TrackMetaData,
    UploadAlbumDto,
)


class RegisterArtistSchema(BaseModel):
    user_id: UUID
    nickname: Annotated[str, Field(max_length=70)]
    avatar_download_url: Annotated[str, Field(max_length=255)]

    def to_dto(self) -> RegisterArtistDto:
        return RegisterArtistDto(
            id=self.user_id,
            nickname=self.nickname,
            avatar_download_url=self.avatar_download_url,
        )


class AlbumMetaDataSchema(BaseModel):
    title: Annotated[str, Field(max_length=70)]
    cover_download_url: Annotated[str, Field(max_length=255)]

    def to_dto(self) -> AlbumMetaData:
        return AlbumMetaData(
            title=self.title,
            cover_download_url=self.cover_download_url,
        )


class TrackMetaDataSchema(BaseModel):
    title: Annotated[str, Field(max_length=70)]
    duration: Annotated[int, Field(gt=0, lte=5 * 60)]
    audio_download_url: Annotated[str, Field(max_length=255)]
    artist_ids: Annotated[set[UUID], Field(min_length=1)]

    def to_dto(self) -> TrackMetaData:
        return TrackMetaData(
            title=self.title,
            duration=self.duration,
            audio_download_url=self.audio_download_url,
            artist_ids=self.artist_ids,
        )


class UploadAlbumSchema(BaseModel):
    album: AlbumMetaDataSchema
    tracks: Iterable[TrackMetaDataSchema]

    def to_dto(self) -> UploadAlbumDto:
        return UploadAlbumDto(
            album=self.album.to_dto(),
            tracks=[track.to_dto() for track in self.tracks],
        )
