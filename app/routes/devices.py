from fastapi import APIRouter

router = APIRouter()


# Obtener información de un dispositivo
@router.get("/get_device", tags=["devices"])
async def get_device(device_id: int) -> dict:  # TODO: Falta seguridad y sacar de la base de datos
    return {'device': device_id}


# Obtener dispositivos de un usuario
@router.get("/get_devices", tags=["devices"])
async def get_devices(user_id: int) -> dict:  # TODO: falta seguridad y sacar de la base de datos
    return {'user_id': user_id}


# Verificar si dispositivo esta registrado
@router.get("/is_device_registered", tags=["devices"])
async def is_device_registered(device_id: str) -> dict:  # TODO: devolver modelo virtual del dispositivo
    return {'device_id': device_id}
