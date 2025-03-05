from fastapi import FastAPI, Depends
from app.routers import auth, dashboard, device_input, filters, admin, profile, notifications, alerts, systems
from app.database import engine, Base
from app.dependencies import get_current_user  # Import authentication function

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="IoT Stream Management Backend", version="1.0")

# Register API routes
app.include_router(auth.router)
app.include_router(dashboard.router, dependencies=[Depends(get_current_user)])
app.include_router(device_input.router, dependencies=[Depends(get_current_user)])
app.include_router(filters.router, dependencies=[Depends(get_current_user)])
app.include_router(admin.router, dependencies=[Depends(get_current_user)])
app.include_router(profile.router, dependencies=[Depends(get_current_user)])
app.include_router(notifications.router, dependencies=[Depends(get_current_user)])
app.include_router(alerts.router, dependencies=[Depends(get_current_user)])
app.include_router(systems.router, dependencies=[Depends(get_current_user)])

@app.get("/")
def health_check():
    return {"message": "IoT Backend is Running!"}
