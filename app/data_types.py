from bson import ObjectId
from pydantic import BaseModel, Extra, Field
from typing import List, Optional, Union


class VirtualModelReading(BaseModel):
    type: str
    readingType: str
    units: str
    dataType: str

    class Config:
        extra = Extra.forbid


class VirtualModelAction(BaseModel):
    type: str


class NewDeviceRegister(BaseModel):
    ownerToken: str
    deviceID: str
    virtualModel: List[Union[VirtualModelReading, VirtualModelAction]]
    additionalInfo: Optional[dict]

    class Config:
        extra = Extra.forbid


class NewDeviceOperation(NewDeviceRegister):
    operation: str

    class Config:
        extra = Extra.forbid


class DeviceVirtualModel(NewDeviceRegister):
    id: str = Field(alias="_id")

    class Config:
        extra = Extra.forbid
