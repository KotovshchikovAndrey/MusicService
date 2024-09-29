from faststream import FastStream

from adapters.driving.rabbitmq.handlers import (
    broker,
    created_artists_queue,
    reviewed_albums_queue,
)

app = FastStream(broker)


@app.after_startup
async def declare_queues():
    await broker.declare_queue(created_artists_queue)
    await broker.declare_queue(reviewed_albums_queue)
