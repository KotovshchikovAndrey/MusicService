from io import BytesIO
from typing import AsyncGenerator, Protocol


class BlobStorage(Protocol):
    async def read(
        self,
        blob_url: str,
        chunk_size: int,
        start_byte: int = 0,
        end_byte: int | None = None,
    ) -> AsyncGenerator[bytes, None]: ...

    async def put(self, blob_url: str, blob: BytesIO) -> None: ...

    async def get_byte_size(self, blob_url: str) -> int: ...
