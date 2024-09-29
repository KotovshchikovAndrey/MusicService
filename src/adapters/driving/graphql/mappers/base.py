from adapters.driving.graphql.schemas.base import JwtPairSchema
from domain.ports.driving.base import JwtPair


def map_to_jwt_pair_schema(data: JwtPair) -> JwtPairSchema:
    return JwtPairSchema(
        access_token=data.access_token,
        refresh_token=data.refresh_token,
    )
