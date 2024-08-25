import enum
from config.ioc_container import container
from pydantic import BaseModel
from domain.usecases.register_artist import RegisterArtistUseCase


class EventType(enum.StrEnum):
    ARTIST_CREATED = "artist_created"


class EventMessage(BaseModel):
    event_type: EventType
    data: dict


class EventMessageDispatcher:
    _register_artist_usecase: RegisterArtistUseCase

    def __init__(self) -> None:
        self._register_artist_usecase = container.resolve(RegisterArtistUseCase)

    async def dispatch(self, event_message: EventMessage) -> None:
        print(event_message.event_type == EventType.ARTIST_CREATED)
