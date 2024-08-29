from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from faststream.rabbit.annotations import RabbitMessage

from adapters.driving.rabbitmq.schemas import (
    RegisterCreatedArtistSchema,
    UploadReviewedAlbumSchema,
)
from config.ioc_container import container
from config.settings import settings
from domain.usecases.register_created_artist import RegisterCreatedArtistUseCase
from domain.usecases.upload_reviewed_album import UploadReviewedAlbumUseCase

broker = RabbitBroker(settings.broker.get_connection_url())

exchange = RabbitExchange(durable=True)

register_created_artist_queue = RabbitQueue(
    name=settings.broker.register_created_artist_queue
)

upload_reviewed_album_queue = RabbitQueue(
    name=settings.broker.upload_reviewed_album_queue
)


@broker.subscriber(
    queue=register_created_artist_queue,
    exchange=exchange,
    retry=True,
)
async def register_created_artist(message: RabbitMessage):
    usecase = container.resolve(RegisterCreatedArtistUseCase)

    try:
        schema = RegisterCreatedArtistSchema.model_validate_json(message.body)
        await usecase.execute(data=schema.to_dto())
    except ValueError as exc:
        # TODO: log invalid format message
        print(exc)
        await message.reject()


@broker.subscriber(
    queue=upload_reviewed_album_queue,
    exchange=exchange,
    retry=True,
)
async def upload_reviwed_album(message: RabbitMessage):
    usecase = container.resolve(UploadReviewedAlbumUseCase)

    try:
        schema = UploadReviewedAlbumSchema.model_validate_json(message.body)
        await usecase.execute(data=schema.to_dto())
    except ValueError as exc:
        # TODO: log invalid format message
        print(exc)
        await message.reject()
