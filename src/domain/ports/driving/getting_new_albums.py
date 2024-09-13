from dataclasses import dataclass, field
from typing import Iterable

from domain.models.entities.album import AlbumInfo
from domain.ports.driving.base import BaseUseCase


@dataclass(frozen=True, kw_only=True, slots=True)
class GetNewAlbumsDto:
    limit: int = field(default=50)


class GetNewAlbumsUseCase(BaseUseCase[GetNewAlbumsDto, Iterable[AlbumInfo]]): ...
