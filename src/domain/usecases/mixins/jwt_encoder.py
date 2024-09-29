import jwt

from domain.models.entities.token import Token
from domain.ports.driving.base import JwtPair


class JwtEncoderMixin:
    def _encode_jwt_pair(self, access_token: Token, refresh_token: Token) -> JwtPair:
        access_token = jwt.encode(
            key=self._access_token_secret,
            payload=access_token.get_payload(),
            algorithm="HS256",
        )

        refresh_token = jwt.encode(
            key=self._refresh_token_secret,
            payload=refresh_token.get_payload(),
            algorithm="HS256",
        )

        return JwtPair(access_token=access_token, refresh_token=refresh_token)
