import json

from domain.events.event_handler import EventHandler
from domain.events.events import UserSignedIn
from domain.ports.driven.message_broker import MessageBroker


class SendVerificationCodeByEmailHandler(EventHandler[UserSignedIn]):
    _broker: MessageBroker
    _email_verification_queue: str

    def __init__(self, broker: MessageBroker, email_verification_queue: str) -> None:
        self._broker = broker
        self._email_verification_queue = email_verification_queue

    async def handle(self, event: UserSignedIn) -> None:
        # TODO: log something

        message = {
            "email": event.user.email.value,
            "code": event.otp_code.code,
        }

        await self._broker.produce(
            queue=self._email_verification_queue,
            message=json.dumps(message),
        )
