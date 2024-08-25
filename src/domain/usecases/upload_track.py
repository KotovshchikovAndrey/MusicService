import hashlib
from io import BytesIO
from typing import Iterable, NewType
from uuid import UUID

from domain.common.exceptions import BadRequestException
from domain.dtos.inputs import UploadTrackDto
from domain.entities.artist import Artist
from domain.entities.track import Track
from domain.factories.track import TrackFactory
from domain.usecases.base import BaseUseCase
from domain.utils.blob_storage import BlobStorage
from domain.utils.moderation import ModerationServiceAdapter
from domain.utils.uow import UnitOfWork

type TrackId = UUID


class UploadTrackUseCase(BaseUseCase[UploadTrackDto, TrackId]):
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

    async def execute(self, data: UploadTrackDto) -> TrackId:
        async with self._uow as uow:
            album = await uow.albums.get_by_id(data.album_id)
            if album is None:
                raise BadRequestException(f"Album with id {data.album_id} not found")

            artists = await uow.artists.filter_by_ids(data.artist_ids)
            if len(data.artist_ids) != len(artists):
                raise BadRequestException("One or more of the 'artist_ids' not found")

        audio = await self._moderation_service.download_approved_audio(
            filename=data.audio_filename
        )

        hashed_audio = hashlib.sha256(audio.getvalue()).hexdigest()
        audio_url = f"/{hashed_audio}.{data.audio_filename.split(".")[-1]}"

        track_factory = TrackFactory(
            album_id=album.id,
            title=data.title,
            duration=data.duration,
            audio_url=audio_url,
        )

        track = track_factory.create()
        await self._save_track(track=track, artists=artists, audio=audio)
        return track.id

    async def _save_track(
        self,
        track: Track,
        artists: Iterable[Artist],
        audio: BytesIO,
    ) -> None:
        artist_ids = tuple(map(lambda artist: artist.id, artists))
        async with self._uow as uow:
            await uow.tracks.upsert(track)
            await uow.tracks.set_artists(track_id=track.id, artist_ids=artist_ids)
            await self._blob_storage.put(blob_url=track.audio_url.value, blob=audio)
            await uow.commit()
