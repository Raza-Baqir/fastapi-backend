from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
# from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.database import get_db
from app.models import User
from app.models import IoTData
from app.schemas import UserCreate, UserLogin, Token, IoTDataCreate
from app.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

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

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# IoT Data Ingestion
router_iot = APIRouter(prefix="/iot", tags=["IoT Data"])

@router_iot.post("/data")
def ingest_iot_data(data: IoTDataCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_data = IoTData(device_id=data.device_id, temperature=data.temperature, humidity=data.humidity, timestamp=datetime.utcnow())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"message": "IoT data stored successfully", "data": new_data}
