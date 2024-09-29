from typing import Annotated

from pydantic import Field

from domain.ports.driving.base import BaseDTO
from domain.ports.driving.user_verification import JwtPair
from domain.usecases.base import BaseUseCase


class RefreshJwtPairDTO(BaseDTO):
    refresh_token: Annotated[str, Field(max_length=150)]


class RefreshJwtPairUseCase(BaseUseCase[RefreshJwtPairDTO, JwtPair]): ...
