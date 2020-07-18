import aio_pika
import logging

from app.rabbit_events.device_management import device_management
from app.config import Settings


# Start of
async def start(settings: Settings):
    connection = await aio_pika.connect_robust(settings.amqp_broker_url)
    logging.info("Connected to RabbitMQ")
    await device_management(connection=connection)