from motor.motor_asyncio import AsyncIOMotorClient
from app.config import Settings
from app.mongo_connection.mongodb import db
import logging


async def start(settings: Settings) -> None:
    db.client = AsyncIOMotorClient(settings.mongodb_url,
                                   serverSelectionTimeoutMS=5000)[settings.mongo_database][settings.mongo_collection]
    logging.info("Created connection to MongoDB, database {} and collection {}".format(settings.mongo_database,
                                                                                       settings.mongo_collection))
