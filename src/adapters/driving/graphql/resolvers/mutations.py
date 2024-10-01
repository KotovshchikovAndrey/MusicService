import strawberry
from fastapi import Request, Response
from strawberry.exceptions import StrawberryGraphQLError

from adapters.driving.graphql.mappers.base import map_to_jwt_pair_schema
from adapters.driving.graphql.schemas.base import JwtPairSchema
from config.ioc_container import container
from domain.errors.token import InvalidRefreshTokenError
from domain.models.entities.token import TokenTTL
from domain.ports.driving.jwt_pair_refreshing import (
    RefreshJwtPairDTO,
    RefreshJwtPairUseCase,
)
from domain.ports.driving.sign_in_process import SignInDTO, SignInUseCase
from domain.ports.driving.user_verification import VerifyUserDTO, VerifyUserUseCase


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def sign_in(self, email: str) -> strawberry.ID:
        usecase = container.resolve(SignInUseCase)
        user_id = await usecase.execute(SignInDTO(email=email))
        return user_id

    @strawberry.mutation
    async def verify_user(
        self,
        email: str,
        otp_code: int,
        info: strawberry.Info,
    ) -> JwtPairSchema:
        request: Request = info.context["request"]
        if "DeviceId" not in request.headers:
            raise StrawberryGraphQLError(message="Missing 'DeviceId' header")

        dto = VerifyUserDTO(
            email=email,
            otp_code=otp_code,
            device_id=request.headers["DeviceId"],
        )

        usecase = container.resolve(VerifyUserUseCase)
        jwt_pair = await usecase.execute(dto)

        response: Response = info.context["response"]
        response.set_cookie(
            key="refresh_token",
            value=jwt_pair.refresh_token,
            httponly=True,
            max_age=TokenTTL.REFRESH_TOKEN,
        )

        return map_to_jwt_pair_schema(jwt_pair)

    @strawberry.mutation
    async def refresh_jwt_pair(self, info: strawberry.Info) -> JwtPairSchema:
        request: Request = info.context["request"]
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token is None:
            raise InvalidRefreshTokenError()

        usecase = container.resolve(RefreshJwtPairUseCase)
        jwt_pair = await usecase.execute(RefreshJwtPairDTO(refresh_token=refresh_token))

        response: Response = info.context["response"]
        response.set_cookie(
            key="refresh_token",
            value=jwt_pair.refresh_token,
            httponly=True,
            max_age=TokenTTL.REFRESH_TOKEN,
        )

        return map_to_jwt_pair_schema(jwt_pair)
