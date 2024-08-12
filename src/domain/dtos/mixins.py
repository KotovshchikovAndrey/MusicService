from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True, slots=True)
class OidMixin:
    oid: str


@dataclass(frozen=True, kw_only=True, slots=True)
class LimitMixin:
    limit: int = field(default=100)
