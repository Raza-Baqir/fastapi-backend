from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Device
from app.schemas import DeviceCreate, DeviceResponse
from app.routers.auth import get_current_user

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/register", response_model=DeviceResponse)
def register_device(device: DeviceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_device = Device(**device.dict(), owner_id=user.id)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.get("/", response_model=List[DeviceResponse])
def get_devices(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Device).filter(Device.owner_id == current_user.id).all()

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    device = db.query(Device).filter(Device.id == device_id, Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, device_update: DeviceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    device = db.query(Device).filter(Device.id == device_id, Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    for key, value in device_update.dict().items():
        setattr(device, key, value)
    
    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    device = db.query(Device).filter(Device.id == device_id, Device.owner_id == current_user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}
