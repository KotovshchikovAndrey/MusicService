from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from faststream.rabbit.annotations import RabbitMessage

from adapters.driving.rabbitmq.schemas import (
    SendOTPCodeByEmailSchema,
    UploadAlbumSchema,
)
from config.ioc_container import container
from config.settings import settings
from domain.ports.driving.album_uploading import UploadAlbumUseCase
from domain.ports.driving.otp_code_sending import SendOTPCodeByEmailUseCase

broker = RabbitBroker(settings.broker.get_connection_url())

exchange = RabbitExchange(durable=True)

albums_to_upload_queue = RabbitQueue(name=settings.broker.albums_to_upload_queue)

email_verification_queue = RabbitQueue(name=settings.broker.email_verification_queue)


@broker.subscriber(
    queue=albums_to_upload_queue,
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


@broker.subscriber(
    queue=email_verification_queue,
    exchange=exchange,
    retry=True,
)
async def send_verification_email(message: RabbitMessage):
    usecase = container.resolve(SendOTPCodeByEmailUseCase)

    try:
        schema = SendOTPCodeByEmailSchema.model_validate_json(message.body)
        await usecase.execute(data=schema.to_dto())
    except ValueError as exc:
        # TODO: log invalid format message
        print(exc)
        await message.reject()
