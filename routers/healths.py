from fastapi import APIRouter, Depends 
from config.security import get_api_key

router = APIRouter(prefix="/api/v1/healths", tags=["Healths"])

@router.get("/")
def health():
    return {
        "status": "You app has a good health ✅"
    }