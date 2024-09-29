from typing import Annotated, Iterable
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, FileUrl

from domain.ports.driving.album_uploading import (
    AlbumMetaData,
    TrackMetaData,
    UploadAlbumDTO,
)
from domain.ports.driving.otp_code_sending import SendOTPCodeByEmailDTO


class AlbumMetaDataSchema(BaseModel):
    title: str
    cover_download_url: FileUrl

    def to_dto(self) -> AlbumMetaData:
        return AlbumMetaData(
            title=self.title,
            cover_download_url=self.cover_download_url,
        )


class TrackMetaDataSchema(BaseModel):
    title: str
    duration: Annotated[int, Field(gt=0)]
    audio_download_url: FileUrl
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

    def to_dto(self) -> UploadAlbumDTO:
        return UploadAlbumDTO(
            album=self.album.to_dto(),
            tracks=[track.to_dto() for track in self.tracks],
        )


class SendOTPCodeByEmailSchema(BaseModel):
    email: EmailStr
    code: str

    def to_dto(self) -> SendOTPCodeByEmailDTO:
        return SendOTPCodeByEmailDTO(
            email=self.email,
            code=self.code,
        )
