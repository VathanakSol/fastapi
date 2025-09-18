from fastapi import FastAPI, HTTPException, Depends, APIRouter
import logging
from contextlib import asynccontextmanager

from schemas.product import Product
from database import Inventory
from config.security import get_api_key
from config.settings import settings

from tortoise import Tortoise, fields, connections
from tortoise.models import Model
from tortoise.exceptions import DBConnectionError

from routers import products, views, healths
from routers import settings as settings_router, connections as connections_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing Postgres Database Connection...")
        await Tortoise.init(
            db_url=settings.database_url,
            modules={"models": ["__main__"]},
        )
        await Tortoise.generate_schemas()
        logger.info("Postgres Database Connection Established Successfully! ✅")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Closing Postgres Database Connections...")
    await Tortoise.close_connections()

# Create Instance
app = FastAPI(
    title="FastAPI Project", 
    version="1.0.0", 
    tags=["Main"],
    lifespan=lifespan
)

# Create Router with Prefix
api_v1 = APIRouter(prefix="/api/v1")

# Register Router for each router services available
app.include_router(products.router)
app.include_router(views.router)
app.include_router(settings_router.router)
app.include_router(connections_router.router)
app.include_router(healths.router)


