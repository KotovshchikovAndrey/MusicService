from domain.dtos.track import ListenTrackDto, AudioStreamDto
from domain.exceptions.not_found import NotFoundException
from domain.utils.blob import BlobStorage
from domain.utils.uow import UnitOfWork
from domain.usecases.base import BaseUseCase


class ListenTrackUseCase(BaseUseCase[ListenTrackDto, AudioStreamDto]):
    _uow: UnitOfWork
    _blob_storage: BlobStorage
    _chunk_size: int

    def __init__(
        self,
        uow: UnitOfWork,
        blob_storage: BlobStorage,
        chunk_size: int,
    ) -> None:
        self._uow = uow
        self._blob_storage = blob_storage
        self._chunk_size = chunk_size

    async def execute(self, data: ListenTrackDto) -> AudioStreamDto:
        async with self._uow as uow:
            track = await uow.tracks.get_by_oid(track_oid=data.oid)
            if track is None:
                raise NotFoundException("Track not found")

        track_size = await self._blob_storage.get_byte_size(track.audio_url.value)
        start_byte, end_byte = data.start_byte, data.end_byte
        if end_byte is None:
            end_byte = track_size

        stream = self._blob_storage.read(
            blob_url=track.audio_url.value,
            chunk_size=self._chunk_size,
            start_byte=start_byte,
            end_byte=end_byte,
        )

        return AudioStreamDto(
            stream=stream,
            content_length=str(end_byte - start_byte),
            content_type="audio/mpeg",
            content_range=f"bytes {start_byte}-{end_byte - 1}/{track_size}",
        )
