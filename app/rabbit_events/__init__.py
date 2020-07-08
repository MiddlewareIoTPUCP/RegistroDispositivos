import asyncio
import aio_pika

from .register_new_device import register_new_device


# Start of
async def start():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    await register_new_device(connection=connection)


if __name__ == "__main__":
    asyncio.run(start())
