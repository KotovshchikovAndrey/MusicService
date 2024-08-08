import hashlib
from io import BytesIO
from typing import Iterable, NewType

from domain.dtos.track import UploadTrackDto
from domain.entities.track import Track
from domain.exceptions.bad_request import BadRequestException
from domain.exceptions.not_found import NotFoundException
from domain.usecases.base import BaseUseCase
from domain.utils.blob import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork

TrackOid = NewType("TrackOid", str)


class UploadTrackUseCase(BaseUseCase[UploadTrackDto, TrackOid]):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _moderation_service: ModerationServiceAdapter

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        moderation_service: ModerationServiceAdapter,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._moderation_service = moderation_service

    async def execute(self, data: UploadTrackDto) -> TrackOid:
        async with self._uow as uow:
            album = await uow.albums.get_by_oid(data.album_oid)
            if album is None:
                raise BadRequestException(f"Album with oid {data.album_oid} not found")

            artists = await uow.artists.filter_by_oids(*data.artist_oids)
            if len(data.artist_oids) != len(artists):
                raise BadRequestException("One or more of the 'artist_oids' not found")

        audio = await self._moderation_service.upload_approved_audio(
            filename=data.audio_filename
        )

        hashed_audio = hashlib.sha256(audio.getvalue()).hexdigest()
        audio_url = f"/{hashed_audio}.{data.audio_filename.split(".")[-1]}"

        track = Track.create(
            album_oid=album.oid.value,
            cover_url=album.cover_url.value,
            title=data.title,
            duration=data.duration,
            audio_url=audio_url,
        )

        await self._save_track(track=track, artists=artists, audio=audio)
        return track.oid.value

    async def _save_track(
        self,
        track: Track,
        artists: Iterable[str],
        audio: BytesIO,
    ) -> None:
        async with self._uow as uow:
            await uow.tracks.upsert(track)
            await uow.tracks.set_track_artists(track.oid.value, *artists)
            await self._blob_storage.put(blob_url=track.audio_url.value, blob=audio)
            await uow.commit()
