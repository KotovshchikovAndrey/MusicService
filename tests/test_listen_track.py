from io import BytesIO
from typing import AsyncGenerator
from unittest import mock
from uuid import uuid4
import pytest

from domain.errors.track import TrackNotFoundError
from domain.models.builders.track import TrackBuilder
from domain.ports.driven.blob_storage import BlobStorage
from domain.ports.driven.database.track_repository import TrackRepository
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.track_listening import ListenTrackDTO
from domain.usecases.listen_track import ListenTrackUseCaseImpl


class FakeBlobStorage(BlobStorage):
    def __init__(self) -> None:
        self._blobs: dict[str, BytesIO] = {}

    async def read(
        self,
        blob_url: str,
        chunk_size: int,
        start_byte: int = 0,
        end_byte: int | None = None,
    ) -> AsyncGenerator[bytes, None]:
        raw_audio = self._blobs[blob_url].getvalue()
        for index in range(start_byte, end_byte or len(raw_audio), chunk_size):
            yield raw_audio[index : index + chunk_size]

    async def put(self, blob_url: str, blob: BytesIO) -> None:
        self._blobs[blob_url] = blob

    async def get_byte_size(self, blob_url: str) -> int:
        return len(self._blobs[blob_url].getvalue())


@pytest.fixture
def mock_uow() -> UnitOfWork:
    mock_uow = mock.MagicMock(spec=UnitOfWork)
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.tracks = mock.MagicMock(spec=TrackRepository)

    return mock_uow


async def test_listen_track_raise_error_when_not_found(mock_uow: UnitOfWork):
    mock_uow.tracks.get_by_id.return_value = None
    usecase = ListenTrackUseCaseImpl(
        uow=mock_uow,
        blob_storage=FakeBlobStorage(),
        chunk_size=1024,
    )

    dto = ListenTrackDTO(track_id=str(uuid4()))
    with pytest.raises(TrackNotFoundError):
        await usecase.execute(dto)


async def test_listen_track_with_byte_range_when_exists(mock_uow: UnitOfWork):
    # Arrange
    audio = BytesIO(b"123456789")
    byte_range = (1, 6)

    fake_blob_storage = FakeBlobStorage()
    await fake_blob_storage.put(blob_url="/test.mp3", blob=audio)

    track = (
        TrackBuilder()
        .set_title("Test Track")
        .set_album(uuid4())
        .set_duration(100)
        .set_audio("/test.mp3")
        .build()
    )

    mock_uow.tracks.get_by_id.return_value = track
    usecase = ListenTrackUseCaseImpl(
        uow=mock_uow,
        blob_storage=fake_blob_storage,
        chunk_size=3,
    )

    dto = ListenTrackDTO(
        track_id=track.id,
        start_byte=byte_range[0],
        end_byte=byte_range[1],
    )

    expected_content_length = str(dto.end_byte - dto.start_byte + 1)
    expected_content_type = "audio/mpeg"

    raw_audio = audio.getvalue()
    audio_size = len(raw_audio)

    expected_content_range = f"bytes {dto.start_byte}-{dto.end_byte}/{audio_size}"
    expected_audio = raw_audio[dto.start_byte : dto.end_byte + 1]

    # Act
    audio_stream = await usecase.execute(dto)

    # Assert
    assert audio_stream.content_length == expected_content_length
    assert audio_stream.content_type == expected_content_type
    assert audio_stream.content_range == expected_content_range

    actual_audio = b""
    async for chunk in audio_stream.stream:
        assert len(chunk) == 3
        actual_audio += chunk

    assert actual_audio == expected_audio
