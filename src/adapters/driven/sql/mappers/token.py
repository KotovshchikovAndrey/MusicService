from datetime import UTC

from adapters.driven.sql.models.token import Token as TokenModel
from domain.models.entities.token import Token


def map_to_token(token_model: TokenModel) -> Token:
    return Token(
        id=token_model.id,
        token_type=token_model.token_type,
        owner_id=token_model.owner_id,
        device_id=token_model.device_id,
        is_revoked=token_model.is_revoked,
        created_at=token_model.created_at.replace(tzinfo=UTC),
        expired_at=token_model.expired_at.replace(tzinfo=UTC),
    )


def map_to_insert_token_values(token: Token) -> dict:
    return {
        "id": token.id.hex,
        "type": token.token_type.value,
        "owner_id": token.owner_id.hex,
        "device_id": token.device_id,
        "is_revoked": token.is_revoked,
        "created_at": token.created_at.replace(tzinfo=None),
        "expired_at": token.expired_at.replace(tzinfo=None),
    }
