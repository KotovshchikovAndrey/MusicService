from typing import Annotated, AsyncGenerator, Self
from uuid import UUID

from pydantic import Field, model_validator

from domain.ports.driving.base import BaseDTO, BaseUseCase


class ListenTrackDTO(BaseDTO):
    track_id: UUID
    start_byte: Annotated[int, Field(default=0, ge=0)]
    end_byte: Annotated[int | None, Field(default=None, ge=0)]

    @model_validator(mode="after")
    def validate_byte_positions(self) -> Self:
        if self.end_byte is None:
            return self

        if self.end_byte <= self.start_byte:
            raise ValueError("The end_byte must be greater than start_byte")

        return self


class AudioStream(BaseDTO, arbitrary_types_allowed=True):
    stream: AsyncGenerator[bytes, None]
    content_type: str
    content_length: str
    content_range: str


class ListenTrackUseCase(BaseUseCase[ListenTrackDTO, AudioStream]): ...
