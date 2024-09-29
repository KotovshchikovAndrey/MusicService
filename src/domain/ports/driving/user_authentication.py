from domain.models.entities.user import AuthenticatedUser
from domain.ports.driving.base import BaseDTO, BaseUseCase


class AuthenticateUserDTO(BaseDTO):
    access_token: str


class AuthenticateUserUseCase(BaseUseCase[AuthenticateUserDTO, AuthenticatedUser]): ...
