from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from faststream.rabbit.annotations import RabbitMessage

from adapters.driving.rabbitmq.schemas import RegisterArtistSchema, UploadAlbumSchema
from config.ioc_container import container
from config.settings import settings
from domain.ports.driving.registering_artists import RegisterArtistUseCase
from domain.ports.driving.uploading_albums import UploadAlbumUseCase

broker = RabbitBroker(settings.broker.get_connection_url())

exchange = RabbitExchange(durable=True)

created_artists_queue = RabbitQueue(name=settings.broker.register_created_artist_queue)

reviewed_albums_queue = RabbitQueue(name=settings.broker.upload_reviewed_album_queue)


@broker.subscriber(
    queue=created_artists_queue,
    exchange=exchange,
    retry=True,
)
async def register_artist(message: RabbitMessage):
    usecase = container.resolve(RegisterArtistUseCase)

    try:
        schema = RegisterArtistSchema.model_validate_json(message.body)
        await usecase.execute(data=schema.to_dto())
    except ValueError as exc:
        # TODO: log invalid format message
        print(exc)
        await message.reject()


@broker.subscriber(
    queue=reviewed_albums_queue,
    exchange=exchange,
    retry=True,
)
async def upload_album(message: RabbitMessage):
    usecase = container.resolve(UploadAlbumUseCase)

    try:
        schema = UploadAlbumSchema.model_validate_json(message.body)
        await usecase.execute(data=schema.to_dto())
    except ValueError as exc:
        # TODO: log invalid format message
        print(exc)
        await message.reject()
