from fastapi import FastAPI, HTTPException, Depends, APIRouter
import logging
from contextlib import asynccontextmanager

from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from config.settings import settings

from tortoise import Tortoise

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
            modules={"models": ["models"]},  # Points to models.py
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake DB
fake_users = {
    "bronak": {
        "username": "user1",
        "hashed_password": pwd_context.hash("123"),
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create Router with Prefix
api_v1 = APIRouter(prefix="/api/v1")

# Verify Password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Create Token for Access
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login Route To Get Access Token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid Username or Password")

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer token"
    }

@app.get("/testing-oauth2-access")
def view_secure_oauth(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return {
        "status": "You are authorized"
    }

# Register Router for each router services available
app.include_router(products.router)
app.include_router(views.router)
app.include_router(settings_router.router)
app.include_router(connections_router.router)
app.include_router(healths.router)


