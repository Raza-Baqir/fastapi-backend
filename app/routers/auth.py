from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import timedelta
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from app.security import get_password_hash, verify_password
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, ResetPasswordRequest, ResetPasswordConfirm

# HTTP Basic Auth
security = HTTPBasic()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Authentication router
router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.get("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": f"Welcome, {user.username}! You are logged in."}

# Forget Password API
reset_tokens = {}  # Temporary storage for reset tokens

@router.post("/forgot-password")
def forgot_password(request: ResetPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = secrets.token_urlsafe(32)
    reset_tokens[user.email] = reset_token
    reset_link = f"http://localhost:8000/auth/reset-password?token={reset_token}"
    
    # Simulate sending an email
    background_tasks.add_task(print, f"Reset your password using this link: {reset_link}")
    return {"message": "Password reset link sent to your email"}

@router.post("/reset-password")
def reset_password(confirm: ResetPasswordConfirm, db: Session = Depends(get_db)):
    for email, token in reset_tokens.items():
        if token == confirm.token:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            user.hashed_password = get_password_hash(confirm.new_password)
            db.commit()
            del reset_tokens[email]
            return {"message": "Password has been reset successfully"}
    
    raise HTTPException(status_code=400, detail="Invalid or expired token")
