from typing import Union, List

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Response, status, Security
from loguru import logger
from pymongo.errors import ServerSelectionTimeoutError

from app.config import get_settings
from app.mongo_connection.mongodb import get_database
from app.utils.hydra_connection import get_current_user
from data_types import DeviceVirtualModel
from app.web_requests.user_service import get_owner_tokens

router = APIRouter()
settings = get_settings()


# Query a device virtual model
@router.get("/get_device", tags=["devices"])
async def get_device(obj_id: str,
                     response: Response,
                     user: str = Security(get_current_user, scopes=["all"])
                     ) -> Union[DeviceVirtualModel, dict]:
    # Getting user owner tokens
    owner_tokens = await get_owner_tokens(user=user)
    if owner_tokens is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": "User doesn't have owner tokens"}

    # Query device from database
    dbClient = await get_database()
    try:
        search_json = {"_id": ObjectId(obj_id)}
        virtualModel = await dbClient.find_one(search_json)
        if virtualModel:
            if virtualModel["ownerToken"] in owner_tokens:
                response.status_code = status.HTTP_200_OK
                # Converting back from ObjectId to str
                virtualModel["_id"] = str(virtualModel["_id"])
                return DeviceVirtualModel(**virtualModel)
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return {"msg": "Can't query that device, not authorized"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"msg": "Device not found"}
    except ServerSelectionTimeoutError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"msg": "Failed connection to MongoDB"}
    except InvalidId:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": "Provided ObjectId is not valid"}


# Query all devices from user
@router.get("/get_devices", tags=["devices"])
async def get_devices(response: Response,
                      user: str = Security(get_current_user, scopes=["all"])
                      ) -> Union[List[DeviceVirtualModel], dict]:
    # Getting user owner tokens
    owner_tokens = await get_owner_tokens(user=user)
    if owner_tokens is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": "User doesn't have owner tokens"}

    # Querying all devices that match the owner_tokens
    dbClient = await get_database()
    try:
        search_json = {"ownerToken": {"$in": owner_tokens}}
        virtualModelsList = list()
        async for virtualModel in dbClient.find(search_json):
            # ObjectId to string
            virtualModel["_id"] = str(virtualModel["_id"])
            virtualModelsList.append(DeviceVirtualModel(**virtualModel))
        response.status_code = status.HTTP_200_OK
        return virtualModelsList
    except ServerSelectionTimeoutError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"msg": "Failed connection to MongoDB"}


# Verify if device is registered
@router.get("/is_device_registered", tags=["devices"])
async def is_device_registered(obj_id: str, owner_token: str, response: Response) -> dict:
    dbClient = await get_database()
    try:
        search_json = {"_id": ObjectId(obj_id)}
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
    except InvalidId:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"msg": "Provided ObjectId is not valid"}
