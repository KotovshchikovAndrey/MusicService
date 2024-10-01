from domain.errors.track import TrackNotFoundError
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.track_listening import (
    AudioStream,
    ListenTrackDTO,
    ListenTrackUseCase,
)


class ListenTrackUseCaseImpl(ListenTrackUseCase):
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

    async def execute(self, data: ListenTrackDTO) -> AudioStream:
        async with self._uow as uow:
            track = await uow.tracks.get_by_id(data.track_id)
            if track is None:
                raise TrackNotFoundError()

        track_size = await self._blob_storage.get_byte_size(track.audio_url.value)
        start_byte, end_byte = data.start_byte, data.end_byte
        if (end_byte is None) or (end_byte > track_size - 1):
            end_byte = track_size - 1

        stream = self._blob_storage.read(
            blob_url=track.audio_url.value,
            chunk_size=self._chunk_size,
            start_byte=start_byte,
            end_byte=end_byte,
        )

        return AudioStream(
            stream=stream,
            content_length=str(end_byte - start_byte + 1),
            content_type="audio/mpeg",
            content_range=f"bytes {start_byte}-{end_byte}/{track_size}",
        )
