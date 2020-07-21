from bson import ObjectId
from fastapi import APIRouter, Response, status
from loguru import logger
from pymongo.errors import ServerSelectionTimeoutError

from app.mongo_connection.mongodb import get_database
from app.data_types import NewDeviceOperation

router = APIRouter()


# Obtener información de un dispositivo
@router.get("/get_device", tags=["devices"])
async def get_device(obj_id: int) -> dict:  # TODO: Falta seguridad y sacar de la base de datos
    return {'device': obj_id}


@router.post("/test", tags=["devices", "test"])
async def test_model(virtual_model: NewDeviceOperation) -> dict:
    return {"virtualModel": virtual_model}


# Obtener dispositivos de un usuario
@router.get("/get_devices", tags=["devices"])
async def get_devices(user_id: int) -> dict:  # TODO: falta seguridad y sacar de la base de datos
    return {'user_id': user_id}


# Verify if device is registered
@router.get("/is_device_registered", tags=["devices"])
async def is_device_registered(obj_id: str, owner_token: str, response: Response) -> dict:
    dbClient = await get_database()
    search_json = {"_id": ObjectId(obj_id)}
    try:
        virtualModel = await dbClient.find_one(search_json)
        if virtualModel:
            if virtualModel["ownerToken"] == owner_token:
                response.status_code = status.HTTP_200_OK
                # Converting back from ObjectId to str
                virtualModel["_id"] = str(virtualModel["_id"])
                return virtualModel
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return {"msg": "Can't query that device, not authorized"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"msg": "Device not found"}
    except ServerSelectionTimeoutError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"msg": "Failed connection to MongoDB"}
