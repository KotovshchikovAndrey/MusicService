from io import BytesIO
from typing import Protocol


class FileDownloader(Protocol):
    async def download_by_url(self, url: str) -> BytesIO: ...
