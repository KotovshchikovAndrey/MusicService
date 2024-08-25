from io import BytesIO
from uuid import uuid4

import pytest

from domain.common.exceptions import NotFoundException
from domain.dtos.inputs import ListenTrackDto
from domain.entities.track import Track
from domain.repositories.track import TrackRepository
from domain.usecases.listen_track import ListenTrackUseCase
from domain.utils.blob_storage import BlobStorage
from domain.utils.uow import UnitOfWork


class TestListenTrackUseCase:
    async def test_play_track_success(
        self,
        track_mock: Track,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        audio_mock: BytesIO,
    ) -> None:
        usecase = ListenTrackUseCase(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        data = ListenTrackDto(id=track_mock.id.hex)
        output = await usecase.execute(data=data)

        buffer = BytesIO()
        async for chunk in output.stream:
            buffer.write(chunk)

        assert audio_mock.getvalue() == buffer.getvalue()

    async def test_track_not_found(
        self,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        track_repository_mock: TrackRepository,
    ) -> None:
        usecase = ListenTrackUseCase(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        track_repository_mock.get_by_id.return_value = None
        with pytest.raises(NotFoundException):
            data = ListenTrackDto(id=uuid4())
            await usecase.execute(data=data)
