# FastAPI Product Management & Database API

A comprehensive REST API built with FastAPI featuring product management, PostgreSQL database integration, and secure API endpoints. This project demonstrates modern FastAPI architecture with modular design, database operations using Tortoise ORM, API security with API keys, dependency injection, and comprehensive CRUD operations.

## Project Structure

```
├── main.py                 # Main FastAPI application with Tortoise ORM integration
├── database.py            # Legacy in-memory database (Inventory dictionary)
├── docker-compose.yml     # PostgreSQL database container setup
├── requirements.txt       # Python dependencies including Tortoise ORM
├── config/
│   ├── settings.py        # Pydantic settings with database URL configuration
│   └── security.py        # API key authentication and security functions
├── schemas/
│   └── product.py         # Pydantic models for data validation
├── routers/
│   ├── products.py        # Product CRUD endpoints (legacy in-memory)
│   ├── connections.py     # Database connection and Item CRUD endpoints
│   ├── views.py           # General view endpoints
│   ├── settings.py        # Settings and environment endpoints
│   └── healths.py         # Health check endpoints
├── .env                   # Environment variables (DATABASE_URL, API_KEY)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore patterns
└── README.md             # Project documentation
```

## Key Components

### `main.py`

- FastAPI application instance with modular router architecture
- **PostgreSQL Integration**: Tortoise ORM setup with async database operations
- **Database Lifecycle Management**: Automatic database initialization and schema generation
- **Router Integration**: Includes routers for products, database operations, views, settings, and health checks
- **Async Context Manager**: Proper database connection handling with lifespan events

### `config/settings.py`

- Pydantic Settings for environment configuration management
- **Database Configuration**: PostgreSQL connection URL management
- **Environment Variables**: Loads from `.env` file for production/development
- Type-safe configuration with automatic validation
- Supports both API key and database URL configuration

### `config/security.py`

- API key authentication using FastAPI Security
- Provides `get_api_key` dependency for protected endpoints
- Integrated with Pydantic settings for dynamic configuration
- Returns proper HTTP 403 errors for invalid keys

### `schemas/product.py`

- Pydantic models for data validation and serialization
- Advanced field validation with constraints
- Type hints for better IDE support and documentation

### `routers/`

- **Modular Route Organization**: Separate APIRouter instances for different functionality
- **Database Operations**: `connections.py` handles PostgreSQL database CRUD operations
- **Product Management**: `products.py` manages legacy in-memory product operations
- **System Monitoring**: `healths.py` provides application health checks
- **Configuration Access**: `settings.py` and `views.py` for system information
- **Consistent API Versioning**: All endpoints use `/api/v1` prefix

### `docker-compose.yml`

- **PostgreSQL Container**: Pre-configured PostgreSQL 15 database
- **Development Ready**: Default credentials and database setup
- **Data Persistence**: Volume mapping for data retention
- **Port Mapping**: Accessible on localhost:5432

## API Endpoints

All protected endpoints require an API key in the `X-API-KEY` header.

### Database Operations (PostgreSQL)

- `GET /api/v1/database/` 🔒 - Test PostgreSQL database connection and get database info
- `POST /api/v1/database/create-items?name={item_name}` 🔒 - Create new item in database
- `GET /api/v1/database/show-items/` 🔒 - Get all items from database
- `GET /api/v1/database/show-items/{item_id}` 🔒 - Get specific item by ID from database
- `DELETE /api/v1/database/remove-items/{item_id}` 🔒 - Delete item from database

### Product Management (Legacy In-Memory)

- `GET /api/v1/product/all` 🔒 - Get all products from inventory
- `GET /api/v1/product/{item_id}` 🔒 - Get specific product by ID
- `POST /api/v1/product/create` 🔒 - Create new product
- `PUT /api/v1/product/update/{item_id}` 🔒 - Update existing product
- `DELETE /api/v1/product/remove/{item_id}` 🔒 - Delete product by ID

### System Endpoints

- `GET /api/v1/healths/` - Application health check (no auth required)
- `GET /api/v1/views/` 🔒 - Secure view endpoint for access verification
- `GET /api/v1/settings/` 🔒 - Get current API key information (development)

## Setup and Installation

### 1. Prerequisites

- Python 3.8+
- Docker and Docker Compose (for PostgreSQL database)

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

Key dependencies include:

- `fastapi` - Web framework
- `tortoise-orm` - Async ORM for database operations
- `asyncpg` - PostgreSQL async driver
- `uvicorn` - ASGI server
- `pydantic-settings` - Configuration management

### 3. Database Setup

```bash
# Start PostgreSQL database using Docker
docker-compose up -d

# This will create a PostgreSQL container with:
# - Database: mydb
# - Username: admin
# - Password: admin
# - Port: 5432
```

### 4. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and configure your settings:
# API_KEY=your_secret_api_key
# DATABASE_URL=postgresql://admin:admin@localhost:5432/mydb
```

### 5. Run the Application

```bash
# Start the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 6. Verify Setup

Test the database connection:

```bash
curl -H "X-API-KEY: your_secret_api_key" http://localhost:8000/api/v1/database/
```

Check application health:

```bash
curl http://localhost:8000/api/v1/healths/
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Key Concepts Implemented

### 1. Advanced Pydantic Models

```python
class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=12)
    price: float = Field(..., gt=1)
    in_stock: bool | None = None
    discount: Optional[float] = None
```

- Field validation with constraints (min/max length, price > 1)
- Optional fields with default values
- Union types for flexible data handling

### 2. API Security with Dependencies

```python
@app.get("/product/all")
def get_all_product(api_key: str = Depends(get_api_key)):
    return Inventory
```

- API key authentication using FastAPI Security
- Dependency injection for reusable security logic
- Automatic HTTP 403 responses for invalid keys

### 3. Dependency Injection for Shared Logic

```python
def common_parameters(q: str | None = None, limit: int = 10):
    return {"q": q, "limit": limit}

@app.get("/views/")
def view_products(commons: dict = Depends(common_parameters)):
    return commons
```

- Reusable parameter logic across endpoints
- Clean separation of concerns
- Reduced code duplication

### 4. Environment Variable Management

```python
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
```

- Secure configuration management
- Environment-specific settings
- Separation of secrets from code

## Common Errors and Solutions

### 403 Forbidden

**Cause**: Invalid or missing API key
**Solutions**:

- Ensure API key is set in `.env` file
- Include `X-API-KEY` header in requests
- Verify API key matches the one in environment variables

### 422 Unprocessable Entity

**Cause**: Data validation failed
**Solutions**:

- Check field names match Pydantic model exactly
- Ensure data types are correct (string, float, boolean)
- Verify required fields are provided
- Check field constraints (name length 2-12, price > 1)

**Example**: Model expects `name` with 2-12 characters, but data has 1 character

### Environment Configuration Issues

**Problem**: API key not loading from `.env` file
**Solutions**:

- Ensure `.env` file exists in project root
- Check `.env` file format: `API_KEY=your_secret_key`
- Verify `python-dotenv` is installed
- Restart the server after changing `.env`

## Data Validation Rules

### Field Name Consistency

- Pydantic model field names must match data dictionary keys
- `in_stock` in model = `"in_stock"` in data (not `"stock"`)

### Type Validation

- FastAPI automatically validates types based on function parameters
- `item_id: int` will reject non-integer values
- Returns 422 error for invalid types

## Best Practices Demonstrated

1. **Separation of Concerns**: Models in separate file from routes
2. **Type Hints**: All functions use proper type annotations
3. **Error Handling**: Proper HTTP status codes and error messages
4. **Route Organization**: Logical grouping of related endpoints
5. **Documentation**: Clear comments explaining each endpoint

## Database Operations Guide

### Database Connection Testing

```bash
# Test PostgreSQL connection and get database info
curl -H "X-API-KEY: your_api_key" http://localhost:8000/api/v1/database/
```

## API Testing Guide

### Prerequisites

1. Start PostgreSQL database:

   ```bash
   docker-compose up -d
   ```

2. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

3. Get your API key from `.env` file

4. Server will be running at `http://localhost:8000`

#### 6. Health Check (No Auth Required)

```bash
curl http://localhost:8000/api/v1/healths/
```

### Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

In Swagger UI, click "Authorize" and enter your API key to test protected endpoints.

### Testing with curl

#### 1. Get All Products

```bash
curl -H "X-API-KEY: dev" http://localhost:8000/api/v1/product/all
```

#### 2. Get Specific Product by ID

```bash
curl -H "X-API-KEY: dev" http://localhost:8000/api/v1/product/1
```

#### 3. Create New Product

```bash
curl -X POST "http://localhost:8000/api/v1/product/create" \
  -H "X-API-KEY: dev" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "price": 29.99,
    "in_stock": true,
    "discount": 0.1
  }'
```

#### 4. Update Product

```bash
curl -X PUT "http://localhost:8000/api/v1/product/update/1" \
  -H "X-API-KEY: dev" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product",
    "price": 39.99,
    "in_stock": false
  }'
```

#### 5. Delete Product

```bash
curl -X DELETE "http://localhost:8000/api/v1/product/remove/1" \
  -H "X-API-KEY: dev"
```

#### 6. Test Access Control

```bash
# Test secure view endpoint
curl -H "X-API-KEY: dev" http://localhost:8000/api/v1/views/

# Test settings endpoint
curl -H "X-API-KEY: dev" http://localhost:8000/api/v1/settings/
```

### Testing with Python requests

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
headers = {"X-API-KEY": "your_api_key"}

# 1. Test database connection
response = requests.get(f"{BASE_URL}/database/", headers=headers)
print("Database connection:", response.json())



# 5. Test health endpoint (no auth required)
response = requests.get(f"{BASE_URL}/healths/")
print("Health check:", response.json())


# 7. Legacy product operations (in-memory)
product_data = {
    "name": "Test Product",
    "price": 19.99,
    "in_stock": True,
    "discount": 0.15
}
response = requests.post(f"{BASE_URL}/product/create",
                        json=product_data, headers=headers)
print("Created product:", response.json())
```

### Testing with Postman

1. **Set Base URL**: `http://localhost:8000/api/v1`

2. **Add Authorization Header**:

   - Key: `X-API-KEY`
   - Value: `your_api_key`

3. **Test Database Endpoints**:

   - GET `/database/` - Test connection

4. **Test System Endpoints**:

   - GET `/healths/` - Health check (no auth)
   - GET `/views/` - Access verification
   - GET `/settings/` - Settings info

5. **Test Legacy Product Endpoints**:
   - GET `/product/all`
   - POST `/product/create` with JSON body
   - PUT `/product/update/1` with JSON body
   - DELETE `/product/remove/1`

### Sample Product JSON

```json
{
  "name": "Sample Product",
  "price": 24.99,
  "in_stock": true,
  "discount": 0.1
}
```

### Expected Responses

#### Success Response (Create/Update)

```json
{
  "status": "Product added successfully",
  "product_id": 1,
  "product": {
    "name": "Sample Product",
    "price": 24.99,
    "in_stock": true,
    "discount": 0.1
  }
}
```

#### Error Response (Invalid API Key)

```json
{
  "detail": "Invalid API Key"
}
```

#### Error Response (Product Not Found)

```json
{
  "detail": "Product Not Found"
}
```

## Recent Updates (Latest)

### PostgreSQL Database Integration

- **Tortoise ORM Integration**: Full async ORM setup with PostgreSQL support
- **Database Lifecycle Management**: Automatic database initialization and schema generation
- **CRUD Operations**: Complete Create, Read, Update, Delete operations for database items
- **Connection Testing**: Built-in database connection testing and health monitoring
- **Docker Integration**: PostgreSQL container setup with docker-compose

### Enhanced API Architecture

- **Database Router**: New `/api/v1/database/` endpoints for PostgreSQL operations
- **Health Monitoring**: Dedicated health check endpoints at `/api/v1/healths/`
- **Dual Data Sources**: Support for both PostgreSQL database and legacy in-memory operations
- **Async Operations**: Full async/await support for database operations
- **Error Handling**: Comprehensive error handling with proper HTTP status codes

### Development Environment

- **Docker Compose**: One-command PostgreSQL database setup
- **Environment Configuration**: Simplified `.env` file configuration
- **Database URL Management**: Secure database connection string handling
- **Development Ready**: Pre-configured database credentials for quick setup

### Security & Configuration

- **Unified Settings**: Single configuration source for API keys and database URLs
- **Protected Endpoints**: API key authentication for all database operations
- **Connection Security**: Masked database URLs in API responses
- **Environment Flexibility**: Support for different environment configurations

## Next Steps for Enhancement

1. **Advanced Database Features**: Add database migrations, indexes, and relationships
2. **JWT Authentication**: Upgrade from API keys to JWT tokens with user management
3. **Rate Limiting**: Add request rate limiting for API protection
4. **Testing**: Add comprehensive unit tests with pytest and database fixtures
5. **Monitoring**: Implement structured logging and metrics collection
6. **Full Containerization**: Dockerize the FastAPI application
7. **API Documentation**: Enhanced OpenAPI documentation with examples
8. **Data Validation**: Advanced input validation and sanitization
9. **Caching**: Implement Redis caching for frequently accessed data
10. **Background Tasks**: Add Celery for asynchronous task processing

## Troubleshooting

### Database Connection Issues

- **PostgreSQL not running**: Ensure Docker container is running with `docker-compose up -d`
- **Connection refused**: Check if PostgreSQL is accessible on port 5432
- **Authentication failed**: Verify database credentials in `.env` file match docker-compose.yml
- **Database doesn't exist**: The database `mydb` should be created automatically by the container

### Server Won't Start

- **Missing dependencies**: Install all requirements with `pip install -r requirements.txt`
- **Environment variables**: Ensure `.env` file exists with `API_KEY` and `DATABASE_URL`
- **Port conflicts**: Check if port 8000 is available or change the port
- **Import errors**: Verify all Python modules are properly installed

### API Key Issues

- **Invalid API Key error**: Ensure `.env` file contains `API_KEY=your_secret_key`
- **Missing header**: Include `X-API-KEY` header in all protected endpoint requests
- **Configuration not loading**: Restart server after modifying `.env` file
- **Pydantic settings**: Verify `pydantic-settings` is installed

### Database Operation Errors

- **Item not found**: Check if the item ID exists in the database
- **Validation errors**: Item names cannot be empty or contain only whitespace
- **Connection timeout**: Verify PostgreSQL container is healthy and accessible
- **Schema issues**: Database tables are created automatically on startup

### Docker Issues

- **Container won't start**: Check Docker daemon is running
- **Port already in use**: Stop other PostgreSQL instances or change port mapping
- **Volume permissions**: Ensure Docker has permission to create volumes
- **Memory issues**: Ensure sufficient system resources for PostgreSQL container

### Common Error Responses

#### 500 Internal Server Error

```json
{
  "detail": "Database connection failed: connection refused"
}
```

**Solution**: Start PostgreSQL with `docker-compose up -d`

#### 403 Forbidden

```json
{
  "detail": "Invalid API Key"
}
```

**Solution**: Add correct `X-API-KEY` header to your request

#### 404 Not Found

```json
{
  "detail": "Item not found"
}
```

**Solution**: Verify the item ID exists in the database

#### 400 Bad Request

```json
{
  "detail": "Item name cannot be empty"
}
```

**Solution**: Provide a valid, non-empty item name

---

_This project demonstrates modern FastAPI development with PostgreSQL integration, async operations, and production-ready architecture patterns._
