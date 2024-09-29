from typing import Annotated, Protocol

from pydantic import BaseModel, Field


class BaseDTO(BaseModel):
    class Config:
        extra = "forbid"
        frozen = True


class Pagination(BaseDTO):
    count: Annotated[int, Field(ge=0)]
    total_count: Annotated[int, Field(ge=0)]
    total_pages: Annotated[int, Field(ge=0)]
    current_page: Annotated[int, Field(gt=0)]
    next_page: Annotated[int | None, Field(default=None, gt=0)]
    prev_page: Annotated[int | None, Field(default=None, gt=0)]


class JwtPair(BaseDTO):
    access_token: str
    refresh_token: str


class BaseUseCase[TInput, TOutput](Protocol):
    async def execute(self, data: TInput) -> TOutput: ...
