from domain.ports.driven.message_broker import MessageBroker


class RabbitMQMessageBroker(MessageBroker):
    async def produce(self, queue: str, message: str) -> None:
        return await super().produce(queue, message)
