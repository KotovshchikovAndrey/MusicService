import pathlib
from io import BytesIO

import aiofiles
import pytest

from domain.dtos.track import ListenTrackDto
from domain.entities.track import Track
from domain.exceptions.not_found import NotFoundException
from domain.usecases.listen_track import ListenTrackUseCase
from domain.utils.blob import BlobStorage
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

        data = ListenTrackDto(oid=track_mock.oid.value)
        output = await usecase.execute(data=data)

        buffer = BytesIO()
        async for chunk in output.stream:
            buffer.write(chunk)

        assert audio_mock.getvalue() == buffer.getvalue()

    async def test_track_not_found(
        self,
        random_oid_mock: str,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
    ) -> None:
        usecase = ListenTrackUseCase(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        with pytest.raises(NotFoundException):
            data = ListenTrackDto(oid=random_oid_mock)
            await usecase.execute(data=data)
