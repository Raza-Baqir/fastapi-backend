from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DeviceBase(BaseModel):
    name: str

class DeviceCreate(DeviceBase):
    name: str
    unique_id: str  # Unique identifier for the device


class DeviceResponse(DeviceBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Enables ORM support for SQLAlchemy models


class IoTDataCreate(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    timestamp: datetime