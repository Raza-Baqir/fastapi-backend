from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app import database, models
from app.utils import verify_password

security = HTTPBasic()  # Initialize HTTP Basic authentication

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security), 
    db: Session = Depends(database.get_db)
):
    """
    Authenticate user using HTTP Basic Authentication.
    """
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user  # Returning the actual User model
