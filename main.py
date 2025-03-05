from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.models import User
from app.routers import auth, devices

from app.routers.iot_data import router as iot_router
from app.routers.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel
# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="IoT Backend", version="1.0")

router = APIRouter()

# Include authentication and device routers
app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(iot_router)
# Pydantic models for user registration and login
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def display_message():
    return {"message": "Backend is running successfully"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "Bearer"}

@app.post("/iot-data/")
async def insert_iot_data(data: dict):
    return {"message": "IoT data inserted successfully"}

app.include_router(router)