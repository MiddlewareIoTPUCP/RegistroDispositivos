from fastapi import APIRouter

router = APIRouter()


# Obtener información de un dispositivo
@router.get("/get_device", tags=["devices"])
async def get_device(device_id: int):  # TODO: Falta seguridad y sacar de la base de datos
    return {'device': device_id}


# Obtener dispositivos de un usuario
@router.get("/get_devices", tags=["devices"])
async def get_devices(user_id: int):  # TODO: falta seguridad y sacar de la base de datos
    return {'user_id': user_id}
