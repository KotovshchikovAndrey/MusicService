import hashlib
from io import BytesIO
from typing import Iterable, NewType

from domain.common.exceptions import BadRequestException
from domain.dtos.inputs import UploadTrackDto
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.factories.track import TrackFactory
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

            artists = await uow.artists.filter_by_oids(data.artist_oids)
            if len(data.artist_oids) != len(artists):
                raise BadRequestException("One or more of the 'artist_oids' not found")

        audio = await self._moderation_service.download_approved_audio(
            filename=data.audio_filename
        )

        hashed_audio = hashlib.sha256(audio.getvalue()).hexdigest()
        audio_url = f"/{hashed_audio}.{data.audio_filename.split(".")[-1]}"

        track_factory = TrackFactory(
            album_oid=album.oid.value,
            title=data.title,
            duration=data.duration,
            audio_url=audio_url,
        )

        track = track_factory.create()
        await self._save_track(track=track, artists=artists, audio=audio)
        return track.oid.value

    async def _save_track(
        self,
        track: Track,
        artists: Iterable[Artist],
        audio: BytesIO,
    ) -> None:
        artist_oids = tuple(map(lambda artist: artist.oid.value, artists))
        async with self._uow as uow:
            await uow.tracks.upsert(track)
            await uow.tracks.set_artists(
                track_oid=track.oid.value,
                artist_oids=artist_oids,
            )

            await self._blob_storage.put(blob_url=track.audio_url.value, blob=audio)
            await uow.commit()
