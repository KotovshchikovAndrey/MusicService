from typing import Protocol


class BaseUseCase[TInput, TOutput](Protocol):
    async def execute(self, data: TInput) -> TOutput: ...
