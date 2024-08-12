from io import BytesIO
from typing import Protocol


class ModerationServiceAdapter(Protocol):
    async def download_approved_audio(self, filename: str) -> BytesIO: ...

    async def download_approved_cover(self, filename: str) -> BytesIO: ...
