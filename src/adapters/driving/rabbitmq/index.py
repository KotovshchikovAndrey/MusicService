from faststream import FastStream

from adapters.driving.rabbitmq.handlers import (
    broker,
    register_created_artist_queue,
    upload_reviewed_album_queue,
)

app = FastStream(broker)


@app.after_startup
async def declare_queues():
    await broker.declare_queue(register_created_artist_queue)
    await broker.declare_queue(upload_reviewed_album_queue)
