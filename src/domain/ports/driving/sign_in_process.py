from uuid import UUID

from pydantic import EmailStr

from domain.ports.driving.base import BaseDTO
from domain.usecases.base import BaseUseCase


class SignInDTO(BaseDTO):
    email: EmailStr


class SignInUseCase(BaseUseCase[SignInDTO, UUID]): ...
