from fastapi import APIRouter

router = APIRouter()

@router.post("/iot-data/")
async def insert_iot_data(data: dict):
    return {"message": "IoT data inserted successfully"}
