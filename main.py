from fastapi import FastAPI, HTTPException, Depends, APIRouter

from schemas.product import Product
from database import Inventory
from config.security import get_api_key
from config.settings import settings

from routers import products, views, settings

# Create Instance
app = FastAPI(title="FastAPI Project", version="1.0.0")

# Create Router with Prefix
api_v1 = APIRouter(prefix="/api/v1")

app.include_router(products.router)
app.include_router(views.router)
app.include_router(settings.router)


