from fastapi import APIRouter, Depends 
from config.security import get_api_key

router = APIRouter(prefix="/api/v1/views", tags=["Views"])

@router.get("/")
def secure_view(api_key: str = Depends(get_api_key)):
    return {
        "status": "You have access ✅"
    }