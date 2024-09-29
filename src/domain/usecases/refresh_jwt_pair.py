from uuid import UUID

import jwt

from domain.exceptions.token import (
    ExpiredRefreshToken,
    InvalidRefreshToken,
    RevokedRefreshToken,
)
from domain.exceptions.user import UserNotFound
from domain.models.entities.token import TokenType
from domain.ports.driven.database.unit_of_work import UnitOfWork
from domain.ports.driving.jwt_pair_refreshing import (
    JwtPair,
    RefreshJwtPairDTO,
    RefreshJwtPairUseCase,
)
from domain.usecases.mixins.jwt_encoder import JwtEncoderMixin


class RefreshJwtPairUseCaseImpl(JwtEncoderMixin, RefreshJwtPairUseCase):
    _uow: UnitOfWork
    _access_token_secret: str
    _refresh_token_secret: str

    def __init__(
        self,
        uow: UnitOfWork,
        access_token_secret: str,
        refresh_token_secret: str,
    ) -> None:
        self._uow = uow
        self._access_token_secret = access_token_secret
        self._refresh_token_secret = refresh_token_secret

    async def execute(self, data: RefreshJwtPairDTO) -> JwtPair:
        payload = self._try_decode_refresh_token(data.refresh_token)
        token_id = UUID(payload["jti"])

        async with self._uow as uow:
            token_in_db = await uow.tokens.get_by_id(token_id)
            if token_in_db is None:
                raise ExpiredRefreshToken()

            if token_in_db.is_revoked:
                await uow.tokens.revoke_by_owner_id(token_in_db.owner_id)
                raise RevokedRefreshToken()

            user = await uow.users.get_by_id(token_in_db.owner_id)
            if user is None:
                raise UserNotFound()

            await uow.tokens.revoke_by_owner_id_and_device_id(
                owner_id=token_in_db.owner_id,
                device_id=token_in_db.device_id,
            )

            access_token, refresh_token = user.issue_token_pair(token_in_db.device_id)
            await uow.tokens.save(refresh_token)

        return self._encode_jwt_pair(access_token, refresh_token)

    def _try_decode_refresh_token(self, refresh_token: str) -> dict:
        try:
            payload: dict = jwt.decode(
                jwt=refresh_token,
                key=self._refresh_token_secret,
                algorithms=["HS256"],
            )

        except jwt.ExpiredSignatureError:
            raise ExpiredRefreshToken()

        except jwt.InvalidTokenError:
            raise InvalidRefreshToken()

        if payload.get("type") != TokenType.REFRESH_TOKEN:
            raise InvalidRefreshToken()

        return payload
