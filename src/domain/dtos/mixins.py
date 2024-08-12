from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True, slots=True)
class OidMixin:
    oid: str


@dataclass(frozen=True, kw_only=True, slots=True)
class LimitMixin:
    limit: int = field(default=100)


@dataclass(frozen=True, kw_only=True, slots=True)
class PageMixin:
    page: int = field(default=1)


@dataclass(frozen=True, kw_only=True, slots=True)
class PaginationMixin:
    count: int
    total_count: int
    total_pages: int
    current_page: int
    next_page: int | None = field(default=None)
    prev_page: int | None = field(default=None)
