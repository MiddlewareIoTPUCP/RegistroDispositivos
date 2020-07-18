from app.mongo_connection.mongodb import get_database
from pymongo.errors import WriteError
import logging


# Searchs in MongoDB if device exists, by ownerToken and deviceID
# and returns its ObjectID if true, else registers new device
async def save_new_device(register_json: dict) -> (int, str):
    dbClient = await get_database()
    # Looks in database for device
    keys_for_search = ["deviceID", "ownerToken"]
    search_json = {x: register_json[x] for x in keys_for_search}
    found = await dbClient.find_one(search_json)
    if found:
        return 200, str(found['_id'])

    # If not found, insert it
    try:
        device_id = await dbClient.insert_one(register_json)
        return 200, str(device_id.inserted_id)
    except WriteError as e:
        # If error is found, especially validation erros of schema, return it
        logging.error(e)
        return 400, str(e)
