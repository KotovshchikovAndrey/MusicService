from typing import Annotated

from pydantic import EmailStr, Field

from domain.ports.driving.base import BaseDTO, JwtPair
from domain.usecases.base import BaseUseCase


class VerifyUserDTO(BaseDTO):
    email: EmailStr
    otp_code: Annotated[int, Field(gt=0)]
    device_id: Annotated[str, Field(min_length=1, max_length=255)]


class VerifyUserUseCase(BaseUseCase[VerifyUserDTO, JwtPair]): ...
