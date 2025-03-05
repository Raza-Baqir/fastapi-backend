from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import DeviceInput, User
from app.schemas import DeviceInputCreate, DeviceInputResponse
from app.utils import verify_password

router = APIRouter(prefix="/device-input", tags=["Device Input Management"])
security = HTTPBasic()  # Initialize HTTP Basic authentication

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """
    Authenticate user using HTTP Basic Authentication.
    """
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user

@router.post("/", response_model=DeviceInputResponse)
def add_device_input(
    device_input: DeviceInputCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Add a new device input (threshold settings like max/min values).
    """
    new_input = DeviceInput(**device_input.dict(), owner_id=current_user.id)
    db.add(new_input)
    db.commit()
    db.refresh(new_input)
    return new_input

@router.get("/", response_model=List[DeviceInputResponse])
def get_device_inputs(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Get all device input settings for the authenticated user.
    """
    return db.query(DeviceInput).filter(DeviceInput.owner_id == current_user.id).all()

@router.put("/{input_id}", response_model=DeviceInputResponse)
def update_device_input(
    input_id: int, 
    device_input_update: DeviceInputCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing device input setting.
    """
    device_input = db.query(DeviceInput).filter(DeviceInput.id == input_id, DeviceInput.owner_id == current_user.id).first()
    if not device_input:
        raise HTTPException(status_code=404, detail="Device input setting not found")

    for key, value in device_input_update.dict().items():
        setattr(device_input, key, value)
    
    db.commit()
    db.refresh(device_input)
    return device_input

@router.delete("/{input_id}")
def delete_device_input(
    input_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Delete a device input setting.
    """
    device_input = db.query(DeviceInput).filter(DeviceInput.id == input_id, DeviceInput.owner_id == current_user.id).first()
    if not device_input:
        raise HTTPException(status_code=404, detail="Device input setting not found")

    db.delete(device_input)
    db.commit()
    return {"message": "Device input setting deleted successfully"}
