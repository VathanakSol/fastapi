# FastAPI Product Management API

A secure REST API built with FastAPI for managing products. This project demonstrates modern FastAPI architecture with modular design, API security with API keys, dependency injection, and comprehensive CRUD operations.

## Project Structure

```
├── main.py                 # Main FastAPI application entry point
├── database.py            # In-memory database (Inventory dictionary)
├── config/
│   ├── settings.py        # Pydantic settings with environment configuration
│   └── security.py        # API key authentication and security functions
├── schemas/
│   └── product.py         # Pydantic models for data validation
├── routers/
│   ├── products.py        # Product CRUD endpoints
│   ├── views.py           # General view endpoints
│   └── settings.py        # Settings and environment endpoints
├── .env                   # Environment variables (not tracked in git)
├── .env.dev              # Development environment variables
├── .env.example          # Environment variables template
└── README.md             # Project documentation
```

## Key Components

### `main.py`

- FastAPI application instance with modular router architecture
- Includes routers for products, views, and settings
- Clean separation of concerns with organized route structure

### `config/settings.py`

- Pydantic Settings for environment configuration management
- Loads from `.env.dev` file for development environment
- Type-safe configuration with automatic validation

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

- Modular route organization with APIRouter
- Separate routers for different functionality areas
- Consistent API versioning with `/api/v1` prefix

## API Endpoints

All endpoints are prefixed with `/api/v1` and require an API key in the `X-API-KEY` header.

### Product Management Endpoints

- `GET /api/v1/product/all` 🔒 - Get all products from inventory
- `GET /api/v1/product/{item_id}` 🔒 - Get specific product by ID
- `POST /api/v1/product/create` 🔒 - Create new product
- `PUT /api/v1/product/update/{item_id}` 🔒 - Update existing product
- `DELETE /api/v1/product/remove/{item_id}` 🔒 - Delete product by ID

### View Endpoints

- `GET /api/v1/views/` 🔒 - Secure view endpoint for access verification

### Settings Endpoints

- `GET /api/v1/settings/` 🔒 - Get current API key information (development)

## Setup and Installation

### 1. Install Dependencies

```bash
# Install required packages
pip install fastapi uvicorn pydantic-settings
```

### 2. Environment Configuration

```bash
# Copy the example environment file
copy .env.example .env.dev

# Edit .env.dev and set your API key
# API_KEY = "dev"
```

The application uses `.env.dev` for development environment configuration.

### 3. Run the Application

```bash
# Start the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

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

## API Testing Guide

### Prerequisites

1. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

2. Get your API key from `.env.dev` file (default: "dev")

3. Server will be running at `http://localhost:8000`

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
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
headers = {"X-API-KEY": "dev"}

# 1. Get all products
response = requests.get(f"{BASE_URL}/product/all", headers=headers)
print("All products:", response.json())

# 2. Create new product
product_data = {
    "name": "Test Product",
    "price": 19.99,
    "in_stock": True,
    "discount": 0.15
}
response = requests.post(f"{BASE_URL}/product/create",
                        json=product_data, headers=headers)
print("Created product:", response.json())

# 3. Get specific product
product_id = 1
response = requests.get(f"{BASE_URL}/product/{product_id}", headers=headers)
print(f"Product {product_id}:", response.json())

# 4. Update product
updated_data = {
    "name": "Updated Product",
    "price": 25.99,
    "in_stock": False
}
response = requests.put(f"{BASE_URL}/product/update/{product_id}",
                       json=updated_data, headers=headers)
print("Updated product:", response.json())

# 5. Test access control
response = requests.get(f"{BASE_URL}/views/", headers=headers)
print("Access test:", response.json())

# 6. Delete product
response = requests.delete(f"{BASE_URL}/product/remove/{product_id}", headers=headers)
print("Deleted product:", response.json())
```

### Testing with Postman

1. **Set Base URL**: `http://localhost:8000/api/v1`

2. **Add Authorization Header**:

   - Key: `X-API-KEY`
   - Value: `dev`

3. **Test Endpoints**:
   - GET `/product/all`
   - GET `/product/1`
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

### Modular Architecture Refactor

- **Router-based Organization**: Separated endpoints into dedicated routers (`products.py`, `views.py`, `settings.py`)
- **API Versioning**: All endpoints now use `/api/v1` prefix for consistent versioning
- **Configuration Management**: Implemented Pydantic Settings with `.env.dev` for development environment
- **Dynamic Configuration**: Security module now uses Pydantic settings for dynamic API key loading

### Enhanced Security

- **Integrated Security**: Security module now uses centralized settings configuration
- **Environment Flexibility**: Support for multiple environment files (`.env`, `.env.dev`)
- **Dynamic API Key Loading**: API key changes in environment files are reflected without code changes (requires server restart)

### Improved Project Structure

- **Schemas Directory**: Moved Pydantic models to dedicated `schemas/` directory
- **Config Directory**: Centralized configuration files in `config/` directory
- **Router Directory**: Organized API endpoints in `routers/` directory
- **Clean Separation**: Clear separation between data models, configuration, and business logic

## Next Steps for Enhancement

1. **Database Integration**: Replace dictionary with SQLAlchemy/databases
2. **JWT Authentication**: Upgrade from API keys to JWT tokens
3. **Rate Limiting**: Add request rate limiting for API protection
4. **Testing**: Add comprehensive unit tests with pytest
5. **Logging**: Implement structured logging for monitoring
6. **Docker**: Add containerization for easy deployment
7. **API Versioning**: Implement API versioning strategy

## Troubleshooting

### Server Won't Start

- Check for syntax errors in Python files
- Ensure all dependencies are installed: `pip install fastapi uvicorn python-dotenv`
- Verify `.env` file exists and contains `API_KEY`
- Check for import errors in modules

### API Key Issues

- Ensure `.env.dev` file is in the project root directory
- Verify API key format in `.env.dev`: `API_KEY=dev` (no quotes)
- Check that `pydantic-settings` is installed
- Restart server after modifying `.env.dev` file
- Default development API key is "dev"

### Validation Errors

- Product name must be 2-12 characters long
- Price must be greater than 1
- Check field names match model exactly
- Ensure JSON content-type header for POST/PUT requests

---

*This project serves as a foundation for understanding FastAPI fundamentals and common API development patterns.*clear
