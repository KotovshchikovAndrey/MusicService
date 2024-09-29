from asyncio import Protocol


class MessageBroker(Protocol):
    async def produce(self, queue: str, message: str) -> None: ...
