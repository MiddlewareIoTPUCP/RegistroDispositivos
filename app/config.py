from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    amqp_broker_url: str = "amqp://guest:guest@localhost:5672/"
    mongodb_url: str = "mongodb://root:root@localhost:27017/"
    mongo_database: str = "IoTMiddleware"
    mongo_collection: str = "devices"
