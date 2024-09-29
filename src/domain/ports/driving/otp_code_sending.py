from pydantic import EmailStr

from domain.ports.driving.base import BaseDTO
from domain.usecases.base import BaseUseCase


class SendOTPCodeByEmailDTO(BaseDTO):
    email: EmailStr
    code: str


class SendOTPCodeByEmailUseCase(BaseUseCase[SendOTPCodeByEmailDTO, None]): ...
