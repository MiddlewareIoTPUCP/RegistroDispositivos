import json

from aio_pika import Connection, Exchange, IncomingMessage, Message
from app.mongo_connection.save_new_device import save_new_device


async def device_management_callback(message: IncomingMessage, exchange: Exchange):
    with message.process():
        register_json: dict = json.loads(message.body)
        if register_json["operation"] == "register":
            register_json.pop("operation", None)
            code, device_id = await save_new_device(register_json)

            headers = {"status": code}
            await exchange.publish(
                Message(body=device_id.encode(), correlation_id=message.correlation_id, headers=headers),
                routing_key=message.reply_to
            )
        else:
            # TODO: Handle unregister and update operation
            pass


async def device_management(connection: Connection):
    async with connection:
        queue_name = "device_management_rpc"
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await device_management_callback(message, channel.default_exchange)
