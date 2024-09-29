from typing import Annotated
from uuid import UUID

from pydantic import Field

from domain.models.entities.artist import Artist
from domain.ports.driving.base import BaseDTO, BaseUseCase


class UpdateArtistDTO(BaseDTO):
    artist_id: UUID
    nickname: Annotated[str | None, Field(default=None)]
    avatar_url: Annotated[str | None, Field(default=None)]


class UpdateArtistUseCase(BaseUseCase[UpdateArtistDTO, Artist]): ...
