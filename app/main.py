import asyncio

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from loguru import logger

from app import rabbit_events
from app.routes import devices
from app import config
from app import mongo_connection
from app.utils.hydra_connection import AuthError

settings = config.get_settings()
app = FastAPI(root_path=settings.root_path)
config.configure_logger()


# Iniciamos la cola de eventos de RabbitMQ
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(rabbit_events.start(settings))
    asyncio.create_task(mongo_connection.start(settings))


@app.exception_handler(AuthError)
def handle_auth_error(request: Request, ex: AuthError):
    return JSONResponse(status_code=ex.status_code, content=ex.error)


# Agregamos las rutas de dispositivos
app.include_router(devices.router)
