import aio_pika
from aio_pika.connection import Connection


async def register_new_device_callback():
    # TODO: save device in MongoDBDatabase
    pass


async def register_new_device(connection: Connection):
    async with connection:
        queue_name = "new_device"
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue_name in message.body.decode():
                        break
