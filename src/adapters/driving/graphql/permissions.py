from typing import Any

from fastapi import Request
from strawberry import BasePermission, Info

from config.ioc_container import container
from domain.errors.user import AuthenticationError
from domain.ports.driving.user_authentication import (
    AuthenticateUserDTO,
    AuthenticateUserUseCase,
)


class IsAuthenticated(BasePermission):
    async def has_permission(self, source: Any, info: Info, **kwargs: Any) -> bool:
        request: Request = info.context["request"]
        if "Authorization" not in request.headers:
            return False

        authorization_header = request.headers["Authorization"]
        if "Bearer " not in authorization_header:
            return False

        access_token = authorization_header.replace("Bearer ", "")
        usecase = container.resolve(AuthenticateUserUseCase)

        data = AuthenticateUserDTO(access_token=access_token)
        authenticated_user = await usecase.execute(data)
        request.state.user = authenticated_user

        return True

    def on_unauthorized(self) -> None:
        raise AuthenticationError()
