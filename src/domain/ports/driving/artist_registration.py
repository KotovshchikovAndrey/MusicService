from uuid import UUID

from domain.ports.driving.base import BaseDTO, BaseUseCase


class RegisterArtistDTO(BaseDTO):
    user_id: UUID
    nickname: str
    avatar_download_url: str


class RegisterArtistUseCase(BaseUseCase[RegisterArtistDTO, UUID]): ...
