from typing import Protocol

from domain.events.events import Event


class EventHandler[T: Event](Protocol):
    async def handle(self, event: T) -> None: ...
