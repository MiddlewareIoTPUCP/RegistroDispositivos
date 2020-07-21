import aio_pika

from loguru import logger

from app.rabbit_events.device_management import device_management
from app.config import Settings


# Start of AioPika connection
async def start(settings: Settings):
    connection = await aio_pika.connect_robust(settings.amqp_broker_url)
    logger.info("Connected to RabbitMQ")
    await device_management(connection=connection)