from io import BytesIO
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.utils.blob import BlobStorage


@pytest.fixture(scope="package")
def blob_storage_mock(audio_mock: BytesIO) -> BlobStorage:
    blob_storage = MagicMock(spec=BlobStorage)

    async def audio_stream() -> AsyncGenerator[bytes, None]:
        for byte in audio_mock:
            yield byte

    blob_storage.read = MagicMock(return_value=audio_stream())
    blob_storage_mock.get_byte_size = AsyncMock(return_value=audio_mock.getvalue())
    return blob_storage
