import typing as tp
from io import BytesIO


class BlobStorage(tp.Protocol):
    async def read(
        self, blob_url: str, chunk_size: int
    ) -> tp.AsyncGenerator[bytes, None]: ...

    async def put(self, blob_url: str, buffer: BytesIO) -> None: ...
