import asyncio

from fastapi import FastAPI

from . import rabbit_events
from .routes import devices

app = FastAPI()


# Iniciamos la cola de eventos de RabbitMQ
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(rabbit_events.start())


# Agregamos las rutas de dispositivos
app.include_router(devices.router)
