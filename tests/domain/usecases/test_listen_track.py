from io import BytesIO
from typing import AsyncGenerator
from uuid import uuid4

import pytest

from domain.errors.track import TrackNotFoundError
from domain.models.entities.track import Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.track_listening import ListenTrackDTO
from domain.usecases.listen_track import ListenTrackUseCaseImpl


class TestListenTrackUseCase:
    @pytest.mark.parametrize(
        "start_byte, end_byte, chunk_size, content_length, content_range",
        (
            (1, 4, 2, "4", "bytes 1-4/5"),
            (1, None, 2, "4", "bytes 1-4/5"),
            (2, 10, 2, "3", "bytes 2-4/5"),
            (2, 4, 1, "3", "bytes 2-4/5"),
        ),
    )
    async def test_play_track_successfully(
        self,
        start_byte: int,
        end_byte: int,
        chunk_size: int,
        content_length: str,
        content_range: str,
        mock_track: Track,
        mock_uow: UnitOfWork,
        mock_audio: BytesIO,
        mock_blob_storage: BlobStorage,
    ) -> None:
        async def read(
            blob_url: str,
            chunk_size: int,
            start_byte: int = 0,
            end_byte: int | None = None,
        ) -> AsyncGenerator[bytes, None]:
            for offset in range(start_byte, end_byte + 1, chunk_size):
                mock_audio.seek(offset)
                yield mock_audio.read(chunk_size)

        mock_blob_storage.read = read
        mock_blob_storage.get_byte_size.return_value = mock_audio.size
        mock_uow.tracks.get_by_id.return_value = mock_track

        usecase = ListenTrackUseCaseImpl(
            uow=mock_uow,
            blob_storage=mock_blob_storage,
            chunk_size=chunk_size,
        )

        data = ListenTrackDTO(
            track_id=mock_track.id,
            start_byte=start_byte,
            end_byte=end_byte,
        )

        output = await usecase.execute(data=data)
        assert output.content_range == content_range
        assert output.content_length == content_length

        buffer = BytesIO()
        async for chunk in output.stream:
            buffer.write(chunk)

        assert len(buffer.getvalue()) == int(output.content_length)

    async def test_track_not_found(
        self,
        mock_uow: UnitOfWork,
        mock_blob_storage: BlobStorage,
    ) -> None:
        usecase = ListenTrackUseCaseImpl(
            uow=mock_uow,
            blob_storage=mock_blob_storage,
            chunk_size=1024,
        )

        mock_uow.tracks.get_by_id.return_value = None
        with pytest.raises(TrackNotFoundError):
            data = ListenTrackDTO(track_id=uuid4())
            await usecase.execute(data=data)
