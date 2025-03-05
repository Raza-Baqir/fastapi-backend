from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("/", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    """
    Get the logged-in user's profile.
    """
    return current_user  # Returns current user's details

@router.put("/", response_model=UserResponse)
def update_profile(user_update: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Update the logged-in user's profile.
    """
    user = db.query(User).filter(User.id == current_user.id).first()

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
