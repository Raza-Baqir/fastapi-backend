from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import device, Notification
from app.schemas import DeviceCreate, DeviceResponse
from app.security import get_current_user
from typing import List

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/register", response_model=DeviceResponse)
def register_device(device: DeviceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_device = device(**device.dict(), owner_id=user.id)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.post("/{device_id}/data")
def add_device_data(device_id: int, value: float, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Add data for a device and check for alerts.
    """
    device = db.query(device).filter(device.id == device_id, device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Check if value exceeds threshold
    if (device.min_value and value < device.min_value) or (device.max_value and value > device.max_value):
        alert_message = f"Alert: {device.name} reported abnormal value {value}"
        
        # Store alert as a notification
        notification = Notification(user_id=current_user.id, message=alert_message)
        db.add(notification)
        db.commit()
    
    return {"message": "Data added successfully"}
