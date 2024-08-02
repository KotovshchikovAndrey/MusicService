from io import BytesIO
import pathlib

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
        track: Track,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
    ) -> None:
        usecase = ListenTrackUseCase(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        buffer = BytesIO()
        output = await usecase.execute(data=ListenTrackDto(oid=track.oid))
        async for chunk in output.stream:
            buffer.write(chunk)

        path = pathlib.Path(".") / "media" / "test_audio.mp3"
        async with aiofiles.open(path, mode="rb") as io:
            audio_file = await io.read()

        assert audio_file == buffer.getvalue()

    async def test_track_not_found(
        self,
        random_oid: str,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
    ) -> None:
        usecase = ListenTrackUseCase(
            uow=uow_mock,
            blob_storage=blob_storage_mock,
            chunk_size=1024,
        )

        with pytest.raises(NotFoundException):
            await usecase.execute(data=ListenTrackDto(oid=random_oid))
