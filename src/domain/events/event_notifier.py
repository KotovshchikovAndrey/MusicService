from domain.events.event_handler import EventHandler
from domain.events.events import Event


class EventNotifier:
    _handlers: dict[Event, list[EventHandler[Event]]]

    def __init__(self) -> None:
        self._handlers = dict()

    async def notify(self, event: Event) -> None:
        if self._handlers.get(type(event)) is None:
            return

        for handler in self._handlers[type(event)]:
            await handler.handle(event)

    async def subscribe(self, event: type[Event], handler: EventHandler) -> None:
        if self._handlers.get(event) is None:
            self._handlers[event] = []

        self._handlers[event].append(handler)
