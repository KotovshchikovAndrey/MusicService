import typing as tp


class BaseUseCase[TInput, TOutput](tp.Protocol):
    async def execute(self, data: TInput) -> TOutput: ...
