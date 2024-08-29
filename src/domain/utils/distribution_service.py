from io import BytesIO
from typing import Protocol


class DistributionServiceAdapter(Protocol):
    async def download_file(self, download_url: str) -> BytesIO: ...
