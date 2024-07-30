from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True, slots=True)
class OidMixin:
    oid: str


@dataclass(frozen=True, kw_only=True, slots=True)
class PaginationMixin:
    limit: int = field(default=100)
    offset: int = field(default=0)
