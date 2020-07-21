from pydantic import BaseModel, Extra
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


class NewDeviceOperation(BaseModel):
    operation: str
    ownerToken: str
    deviceID: str
    virtualModel: List[Union[VirtualModelReading, VirtualModelAction]]
    additionalInfo: Optional[dict]

    class Config:
        extra = Extra.forbid


class NewDeviceRegister(BaseModel):
    ownerToken: str
    deviceID: str
    virtualModel: List[Union[VirtualModelReading, VirtualModelAction]]
    additionalInfo: Optional[dict]

    class Config:
        extra = Extra.forbid
