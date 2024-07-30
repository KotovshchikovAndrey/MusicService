from io import BytesIO
import pathlib

import aiofiles
import pytest

from domain.dtos.track import PlayTrackDto
from domain.entities.track import Track
from domain.exceptions.not_found import NotFoundException
from domain.usecases.play_track import PlayTrackUseCase
from domain.utils.blob import BlobStorage
from domain.utils.uow import UnitOfWork


class TestPlayTrackUseCase:
    async def test_play_track_success(
        self,
        track: Track,
        uow_mock: UnitOfWork,
        blob_storage_mock: BlobStorage,
    ) -> None:
        buffer = BytesIO()
        usecase = PlayTrackUseCase(uow=uow_mock, blob_storage=blob_storage_mock)
        async for chunk in usecase.execute(data=PlayTrackDto(oid=track.oid)):
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
        usecase = PlayTrackUseCase(uow=uow_mock, blob_storage=blob_storage_mock)
        with pytest.raises(NotFoundException):
            await anext(usecase.execute(data=PlayTrackDto(oid=random_oid)))
