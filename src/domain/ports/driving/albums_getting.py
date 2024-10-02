from typing import Annotated

from pydantic import Field

from domain.models.entities.album import AlbumInfo
from domain.ports.driving.base import BaseDTO, BaseUseCase


class GetAlbumsDTO(BaseDTO):
    limit: Annotated[int, Field(default=50, gt=0, le=100)]


class GetAlbumsUseCase(BaseUseCase[GetAlbumsDTO, list[AlbumInfo]]): ...
