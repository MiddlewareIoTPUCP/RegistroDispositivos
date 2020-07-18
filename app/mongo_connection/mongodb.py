from motor.motor_asyncio import AsyncIOMotorClient


class MongoDataBase:
    client: AsyncIOMotorClient = None


db = MongoDataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client
