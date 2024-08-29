from typing import Annotated, Iterable
from uuid import UUID

from pydantic import BaseModel, Field

from domain.dtos.inputs import (
    RegisterCreatedArtistDto,
    UploadAlbumDto,
    UploadReviewedAlbumDto,
    UploadTrackDto,
)


class RegisterCreatedArtistSchema(BaseModel):
    user_id: UUID
    nickname: Annotated[str, Field(max_length=70)]
    avatar_download_url: Annotated[str, Field(max_length=255)]

    def to_dto(self) -> RegisterCreatedArtistDto:
        return RegisterCreatedArtistDto(
            id=self.user_id,
            nickname=self.nickname,
            avatar_download_url=self.avatar_download_url,
        )


class UploadAlbumSchema(BaseModel):
    title: Annotated[str, Field(max_length=70)]
    cover_download_url: Annotated[str, Field(max_length=255)]

    def to_dto(self) -> UploadAlbumDto:
        return UploadAlbumDto(
            title=self.title,
            cover_download_url=self.cover_download_url,
        )


class UploadTrackSchema(BaseModel):
    title: Annotated[str, Field(max_length=70)]
    duration: Annotated[int, Field(gt=0, lte=5 * 60)]
    audio_download_url: Annotated[str, Field(max_length=255)]
    artist_ids: Annotated[set[UUID], Field(min_length=1)]

    def to_dto(self) -> UploadTrackDto:
        return UploadTrackDto(
            title=self.title,
            duration=self.duration,
            audio_download_url=self.audio_download_url,
            artist_ids=self.artist_ids,
        )


class UploadReviewedAlbumSchema(BaseModel):
    album: UploadAlbumSchema
    tracks: Iterable[UploadAlbumSchema]

    def to_dto(self) -> UploadReviewedAlbumDto:
        return UploadReviewedAlbumDto(
            album=self.album.to_dto(),
            tracks=[track.to_dto() for track in self.tracks],
        )
