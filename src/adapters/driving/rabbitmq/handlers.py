from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from faststream.rabbit.annotations import RabbitMessage

from adapters.driving.rabbitmq.dispatcher import EventMessage, EventMessageDispatcher
from config.settings import settings

broker = RabbitBroker(settings.broker.get_connection_url())

exchange = RabbitExchange(durable=True)

distribution_queue = RabbitQueue(settings.broker.distribution_queue)

dispatcher = EventMessageDispatcher()


@broker.subscriber(
    queue=distribution_queue,
    exchange=exchange,
    retry=True,
)
async def handle_distribution_events(message: RabbitMessage):
    try:
        event_message = EventMessage.model_validate_json(message.body)
        await dispatcher.dispatch(event_message)

    except ValueError as exc:
        # TODO: log invalid format message
        print(exc)
        await message.reject()

    await message.reject()
