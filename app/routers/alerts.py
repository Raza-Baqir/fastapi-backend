from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Notification
from app.schemas import NotificationResponse
from app.dependencies import get_current_user  # Import authentication dependency

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=List[NotificationResponse])
def get_alerts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Fetch all alerts for the current user.
    """
    return db.query(Notification).filter(Notification.user_id == current_user.id).all()
