from loguru import logger
from pymongo.errors import WriteError, ServerSelectionTimeoutError

from app.mongo_connection.mongodb import get_database
from app.web_requests.user_service import check_owner_token


# Searchs in MongoDB if device exists, by ownerToken and deviceID
# and returns its ObjectID if true, else registers new device
async def save_new_device(register_json: dict) -> (int, str):
    ownerToken = register_json["ownerToken"]
    exists = check_owner_token(ownerToken)

    if not exists:
        return 400, "Owner Token doesn't exist"

    dbClient = await get_database()
    # Looks in database for device
    keys_for_search = ["deviceID", "ownerToken"]
    search_json = {x: register_json[x] for x in keys_for_search}
    try:
        found = await dbClient.find_one(search_json)
        if found:
            return 200, str(found["_id"])
    except ServerSelectionTimeoutError as e:
        logger.error("Failed to connect to MongoDB, exiting")
        return 500, str(e)

    # If not found, insert it
    try:
        device_id = await dbClient.insert_one(register_json)
        return 200, str(device_id.inserted_id)
    except WriteError as e:
        # If error is found, especially validation errors of schema, return 400
        return 400, str(e)
    except ServerSelectionTimeoutError as e:
        logger.error("Failed to connect to MongoDB, exiting")
        return 500, str(e)
