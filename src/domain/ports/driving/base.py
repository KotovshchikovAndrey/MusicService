from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True, kw_only=True, slots=True)
class PaginationMixin:
    count: int
    total_count: int
    total_pages: int
    current_page: int
    next_page: int | None = field(default=None)
    prev_page: int | None = field(default=None)


class BaseUseCase[TInput, TOutput](Protocol):
    async def execute(self, data: TInput) -> TOutput: ...
