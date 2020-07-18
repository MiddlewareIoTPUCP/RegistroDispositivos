from motor.motor_asyncio import AsyncIOMotorClient
from app.config import Settings
from app.mongo_connection.mongodb import db
import logging


async def start(settings: Settings) -> None:
    db.client = AsyncIOMotorClient(settings.mongodb_url)[settings.mongo_database][settings.mongo_collection]
    logging.info("Connected to MongoDB and database %s collection %s".format(settings.mongo_database))
