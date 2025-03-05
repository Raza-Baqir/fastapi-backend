from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)  # Increased length
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    systems = relationship("System", back_populates="owner", cascade="all, delete-orphan")
    device_inputs = relationship("DeviceInput", back_populates="owner", cascade="all, delete-orphan")
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

class System(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)  # Increased length
    widget_type = Column(String(50), nullable=False)  # "map", "chart", "indicator"
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="systems")
    devices = relationship("Device", back_populates="system", cascade="all, delete-orphan")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    system_id = Column(Integer, ForeignKey("systems.id"), nullable=False)
    status = Column(Boolean, default=True)

    system = relationship("System", back_populates="devices")
    device_inputs = relationship("DeviceInput", back_populates="device", cascade="all, delete-orphan")

class DeviceInput(Base):
    __tablename__ = "device_inputs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    parameter = Column(String(50), nullable=False)  # e.g., "Temperature"
    min_value = Column(Float, nullable=False)
    max_value = Column(Float, nullable=False)
    alert_enabled = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="device_inputs")
    device = relationship("Device", back_populates="device_inputs")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)  # Increased length
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="notifications")

class IoTData(Base):
    __tablename__ = "iot_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=False)  # Foreign key if applicable
    sensor_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)