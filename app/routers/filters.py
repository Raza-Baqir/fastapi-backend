from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Device, DeviceInput
from app.schemas import DeviceResponse, DeviceInputResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/filter", tags=["Filtering"])

@router.get("/devices", response_model=List[DeviceResponse])
def filter_devices(
    device_type: Optional[str] = Query(None, description="Filter by device type"),
    registered_after: Optional[datetime] = Query(None, description="Filter by registration date"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Filter devices based on type and registration date.
    """
    query = db.query(Device).filter(Device.owner_id == current_user.id)

    if device_type:
        query = query.filter(Device.type == device_type)

    if registered_after:
        query = query.filter(Device.created_at >= registered_after)

    return query.all()

@router.get("/device-inputs", response_model=List[DeviceInputResponse])
def filter_device_inputs(
    device_id: Optional[int] = Query(None, description="Filter by device ID"),
    parameter: Optional[str] = Query(None, description="Filter by parameter type"),
    min_value: Optional[float] = Query(None, description="Filter values greater than this"),
    max_value: Optional[float] = Query(None, description="Filter values less than this"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Filter device input settings based on parameters.
    """
    query = db.query(DeviceInput).filter(DeviceInput.owner_id == current_user.id)

    if device_id:
        query = query.filter(DeviceInput.device_id == device_id)

    if parameter:
        query = query.filter(DeviceInput.parameter == parameter)

    if min_value is not None:
        query = query.filter(DeviceInput.min_value >= min_value)

    if max_value is not None:
        query = query.filter(DeviceInput.max_value <= max_value)

    return query.all()
