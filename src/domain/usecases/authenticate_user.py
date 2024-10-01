import jwt

from domain.errors.token import ExpiredAccessTokenError, InvalidAccessTokenError
from domain.errors.user import AuthenticationError
from domain.models.entities.token import BaseToken, TokenType
from domain.models.entities.user import AuthenticatedUser
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.user_authentication import (
    AuthenticateUserDTO,
    AuthenticateUserUseCase,
)


class AuthenticateUseUseCaseImpl(AuthenticateUserUseCase):
    _uow: UnitOfWork
    _access_token_secret: str

    def __init__(self, uow: UnitOfWork, access_token_secret: str) -> None:
        self._uow = uow
        self._access_token_secret = access_token_secret

    async def execute(self, data: AuthenticateUserDTO) -> AuthenticatedUser:
        payload = self._try_decode_access_token(data.access_token)
        token = BaseToken.from_payload(payload)
        async with self._uow as uow:
            user = await uow.users.get_by_id(token.owner_id)
            if user is None:
                raise AuthenticationError()

        return AuthenticatedUser(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            token=token,
        )

    def _try_decode_access_token(self, access_token: str) -> dict:
        try:
            payload: dict = jwt.decode(
                jwt=access_token,
                algorithms=["HS256"],
                key=self._access_token_secret,
            )

        except jwt.ExpiredSignatureError:
            raise ExpiredAccessTokenError()

        except jwt.InvalidTokenError:
            raise InvalidAccessTokenError()

        if payload.get("type") != TokenType.ACCESS_TOKEN:
            raise InvalidAccessTokenError()

        return payload
