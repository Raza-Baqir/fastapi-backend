from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Device, User
from app.schemas import DeviceResponse
from app.utils import verify_password

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
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

@router.get("/", response_model=List[DeviceResponse])
def get_dashboard_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetch all devices owned by the authenticated user and return their data.
    """
    devices = db.query(Device).filter(Device.owner_id == current_user.id).all()
    
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found for the user")
    
    return devices
