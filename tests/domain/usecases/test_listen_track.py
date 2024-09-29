from io import BytesIO
from typing import AsyncGenerator
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from domain.exceptions.track import TrackNotFound
from domain.models.entities.track import Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.track_repository import TrackRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.track_listening import ListenTrackDTO
from domain.usecases.listen_track import ListenTrackUseCaseImpl


class TestListenTrackUseCase:
    @pytest.mark.parametrize(
        "start_byte, end_byte, chunk_size, content_length,  content_range",
        (
            (1, 4, 2, "4", "bytes 1-4/5"),
            (1, None, 2, "4", "bytes 1-4/5"),
            (2, 10, 2, "3", "bytes 2-4/5"),
        ),
    )
    async def test_play_track_successfully(
        self,
        start_byte: int,
        end_byte: int,
        chunk_size: int,
        content_length: str,
        content_range: str,
        track_mock: Track,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        audio_mock: BytesIO,
    ) -> None:
        async def read(
            blob_url: str,
            chunk_size: int,
            start_byte: int = 0,
            end_byte: int | None = None,
        ) -> AsyncGenerator[bytes, None]:
            for offset in range(start_byte, end_byte + 1, chunk_size):
                audio_mock.seek(offset)
                yield audio_mock.read(chunk_size)

        blob_storage_mock.read = read
        blob_storage_mock.get_byte_size = AsyncMock(return_value=audio_mock.size)

        usecase = ListenTrackUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=chunk_size,
        )

        data = ListenTrackDTO(
            track_id=track_mock.id,
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
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        track_repository_mock: TrackRepository,
    ) -> None:
        usecase = ListenTrackUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        track_repository_mock.get_by_id.return_value = None
        with pytest.raises(TrackNotFound):
            data = ListenTrackDTO(track_id=uuid4())
            await usecase.execute(data=data)
