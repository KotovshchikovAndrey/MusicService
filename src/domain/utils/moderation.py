from io import BytesIO
from typing import Protocol


class ModerationServiceAdapter(Protocol):
    async def upload_approved_audio(self, filename: str) -> BytesIO: ...

    async def upload_approved_cover(self, filename: str) -> BytesIO: ...
