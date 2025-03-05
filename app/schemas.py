from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# Schema for User Login
class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    email: Optional[str] = None

class ResetPasswordRequest(BaseModel): 
    email: str

class ResetPasswordConfirm(BaseModel):  
    token: str
    new_password: str

class SystemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    widget_type: str  # Example: "map", "chart", "indicator"

class SystemResponse(SystemCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class DeviceInputCreate(BaseModel):
    device_id: int
    parameter: str  # e.g., "Temperature", "Humidity"
    min_value: float
    max_value: float
    alert_enabled: bool

class DeviceInputResponse(DeviceInputCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class NotificationResponse(BaseModel):
    id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True

class DeviceCreate(BaseModel):
    name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None

class DeviceResponse(DeviceCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True