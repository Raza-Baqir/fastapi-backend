from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import System
from app.schemas import SystemCreate, SystemResponse
from app.dependencies import get_current_user
from app.routers import __init__

router = APIRouter(prefix="/system", tags=["System Management"])

def some_function():
    from app.routers import dashboard  # Import inside function
    return dashboard.some_function()

@router.post("/", response_model=SystemResponse)
def add_system(system: SystemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Add a new IoT system with related widgets (maps, charts, indicators).
    """
    new_system = System(**system.dict(), owner_id=current_user.id)
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system

@router.get("/", response_model=List[SystemResponse])
def get_systems(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get all IoT systems owned by the authenticated user.
    """
    return db.query(System).filter(System.owner_id == current_user.id).all()

@router.put("/{system_id}", response_model=SystemResponse)
def update_system(system_id: int, system_update: SystemCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Update an existing IoT system.
    """
    system = db.query(System).filter(System.id == system_id, System.owner_id == current_user.id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    for key, value in system_update.dict().items():
        setattr(system, key, value)
    
    db.commit()
    db.refresh(system)
    return system

@router.delete("/{system_id}")
def delete_system(system_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Delete an IoT system.
    """
    system = db.query(System).filter(System.id == system_id, System.owner_id == current_user.id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    db.delete(system)
    db.commit()
    return {"message": "System deleted successfully"}
