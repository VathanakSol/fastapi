from fastapi import APIRouter, Depends
from config.security import get_api_key
from config.settings import settings

router = APIRouter(prefix="/api/v1/settings", tags=["Environment"])

# View Own Key (Dev)
@router.get("/")
def settings(api_key: str = Depends(get_api_key)):
    return {
        "api_key": api_key,
    }