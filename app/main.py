import asyncio

from fastapi import FastAPI

from app import rabbit_events
from app.routes import devices
from app import config
from app import mongo_connection

app = FastAPI()
settings = config.Settings()


# Iniciamos la cola de eventos de RabbitMQ
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(rabbit_events.start(settings))
    asyncio.create_task(mongo_connection.start(settings))


# Agregamos las rutas de dispositivos
app.include_router(devices.router)
