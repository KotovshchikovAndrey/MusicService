import typing as tp
from dataclasses import dataclass, field
from domain.dtos.base import OidMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtistDto(OidMixin):
    fullname: str
