from fastapi import APIRouter, HTTPException, Depends
from config.security import get_api_key
from config.settings import settings
from tortoise import connections
from tortoise.models import Model
from tortoise import fields
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/database", tags=["Database Connection"])

# Testing Postgres Database Connection
@router.get("/")
async def test_db_connection(api_key: str = Depends(get_api_key)):
    """Test database connection and return connection status"""
    try:
        connection = connections.get("default")
        await connection.execute_query("SELECT 1")
        
        # Get database info
        db_info = await connection.execute_query("SELECT version()")
        
        return {
            "status": "success",
            "message": "It works ✅",
            "database_info": db_info[1][0][0] if db_info[1] else "Unknown",
            "connection_url": settings.database_url.replace(settings.database_url.split('@')[0].split('//')[1], "***:***")
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed: {str(e)}"
        )



