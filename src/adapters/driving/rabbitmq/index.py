from faststream import FastStream

from adapters.driving.rabbitmq.handlers import broker, distribution_queue

app = FastStream(broker)


@app.after_startup
async def declare_queues():
    await broker.declare_queue(distribution_queue)
