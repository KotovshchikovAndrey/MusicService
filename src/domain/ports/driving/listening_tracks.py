from dataclasses import dataclass, field
from typing import AsyncGenerator
from uuid import UUID

from domain.ports.driving.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class ListenTrackDto:
    track_id: UUID
    start_byte: int = field(default=0)
    end_byte: int | None = field(default=None)


@dataclass(frozen=True, kw_only=True, slots=True)
class AudioStream:
    stream: AsyncGenerator[bytes, None]
    content_type: str
    content_length: str
    content_range: str


class ListenTrackUseCase(BaseUseCase[ListenTrackDto, AudioStream]): ...
