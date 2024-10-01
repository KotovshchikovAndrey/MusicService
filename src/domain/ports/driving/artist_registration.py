from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, HttpUrl

from domain.ports.driving.base import BaseDTO, BaseUseCase


class RegisterArtistDTO(BaseDTO):
    user_id: UUID
    nickname: str
    avatar_url: Annotated[HttpUrl, AfterValidator(func=lambda url: str(url))]


class RegisterArtistUseCase(BaseUseCase[RegisterArtistDTO, UUID]): ...
