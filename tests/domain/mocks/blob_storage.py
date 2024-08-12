# from io import BytesIO
# from typing import AsyncGenerator

# from domain.utils.blob import BlobStorage


# class MockedBlobStorage(BlobStorage):
#     _blobs: dict[str, BytesIO]

#     def __init__(self, blobs: list[BytesIO]) -> None:
#         self._blobs = {blob.name: blob for blob in blobs}

# async def read(
#     self,
#     blob_url: str,
#     chunk_size: int,
#     start_byte: int = 0,
#     end_byte: int | None = None,
# ) -> AsyncGenerator[bytes, None]:
#     blob = self._blobs[blob_url.replace("/", "")]
#     for byte in blob:
#         yield byte

# async def put(self, blob_url: str, blob: BytesIO) -> None:
#     self._blobs[blob_url.replace("/", "")] = blob

# async def get_byte_size(self, blob_url: str) -> int:
#     blob = self._blobs[blob_url.replace("/", "")]
#     return len(blob.getvalue())


from io import BytesIO
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.utils.blob import BlobStorage


@pytest.fixture(scope="package")
def blob_storage_mock(audio_mock: BytesIO) -> BlobStorage:
    blob_storage = MagicMock(spec=BlobStorage)

    async def audio_stream():
        for byte in audio_mock:
            yield byte

    blob_storage.read = MagicMock(return_value=audio_stream())
    blob_storage_mock.get_byte_size = AsyncMock(return_value=audio_mock.getvalue())
    return blob_storage
