import typing as tp

from config.settings import settings
from domain.dtos.track import PlayTrackDto
from domain.exceptions.not_found import NotFoundException
from domain.utils.blob import BlobStorage
from domain.utils.uow import UnitOfWork
from domain.usecases.base import BaseUseCase


class PlayTrackUseCase(BaseUseCase[PlayTrackDto, tp.AsyncGenerator[bytes, None]]):
    _uow: UnitOfWork
    _blob_storage: BlobStorage

    def __init__(self, uow: UnitOfWork, blob_storage: BlobStorage) -> None:
        self._uow = uow
        self._blob_storage = blob_storage

    async def execute(self, data: PlayTrackDto) -> tp.AsyncGenerator[bytes, None]:
        async with self._uow as uow:
            track = await uow.tracks.get_one(track_oid=data.oid)
            if track is None:
                raise NotFoundException("Track not found")

            async for chunk in self._blob_storage.read(
                blob_url=track.audio_url.value,
                chunk_size=settings.audio_play_chunk_size,
            ):
                yield chunk
