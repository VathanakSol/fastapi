from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from .settings import settings

api_key_header = APIKeyHeader(name="X-API-KEY")

# Dependency to check API Key
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key