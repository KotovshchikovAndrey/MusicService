from io import BytesIO
from uuid import uuid4

import pytest

from domain.exceptions.track import TrackNotFound
from domain.models.entities.track import Track
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.track_repository import TrackRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.listening_tracks import ListenTrackDto
from domain.usecases.listen_track import ListenTrackUseCaseImpl


class TestListenTrackUseCase:
    async def test_play_track_success(
        self,
        track_mock: Track,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
        audio_mock: BytesIO,
    ) -> None:
        usecase = ListenTrackUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        data = ListenTrackDto(track_id=track_mock.id.hex)
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
        usecase = ListenTrackUseCaseImpl(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        track_repository_mock.get_by_id.return_value = None
        with pytest.raises(TrackNotFound):
            data = ListenTrackDto(track_id=uuid4())
            await usecase.execute(data=data)
