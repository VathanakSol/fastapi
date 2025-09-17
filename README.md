# FastAPI Product Management API

A secure REST API built with FastAPI for managing products. This project demonstrates core FastAPI concepts, API security with API keys, dependency injection, and comprehensive CRUD operations.

## Project Structure

```
├── main.py          # Main FastAPI application with route definitions
├── product.py       # Pydantic models and data storage
├── security.py      # API key authentication and security functions
├── .env             # Environment variables (not tracked in git)
├── .env.example     # Environment variables template
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## Key Files

### `main.py`

- Contains the FastAPI application instance
- Defines all API endpoints with security protection
- Implements full CRUD operations (GET, POST, PUT, DELETE)
- Uses dependency injection for shared logic and security
- Handles error handling with HTTPException

### `product.py`

- Defines the `Product` Pydantic model with advanced validation
- Contains the `Inventory` dictionary (fake database)
- Implements field validation with constraints (min/max length, price validation)
- Supports optional fields like discount

### `security.py`

- Implements API key authentication using FastAPI Security
- Provides `get_api_key` dependency for protected endpoints
- Loads API key from environment variables
- Returns proper HTTP 403 errors for invalid keys

## API Endpoints

### Security-Protected Endpoints

All endpoints marked with 🔒 require an API key in the `X-API-KEY` header.

### General Endpoints

- `GET /views/` - View products with shared parameters (q, limit)
- `GET /views/secure/` 🔒 - Secure endpoint demonstrating API key access
- `GET /info` 🔒 - Get testing information

### Product Endpoints

- `GET /product/name/{product_name}` - Get product by name (public)
- `GET /product/all` 🔒 - Get all products from inventory
- `GET /product/{item_id}` 🔒 - Get specific product by ID
- `POST /product/create/` 🔒 - Create new product
- `PUT /product/update/{item_id}` 🔒 - Update existing product
- `DELETE /product/remove/{item_id}` 🔒 - Delete product by ID

## Setup and Installation

### 1. Install Dependencies

```bash
# Install required packages
pip install fastapi uvicorn python-dotenv
```

### 2. Environment Configuration

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and set your API key
# API_KEY = "your_secret_key_here"
```

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

## Testing the API

### Using curl

```bash
# Public endpoint (no API key required)
curl http://localhost:8000/product/name/Product1

# Protected endpoints (API key required)
curl -H "X-API-KEY: your_secret_key" http://localhost:8000/product/all
curl -H "X-API-KEY: your_secret_key" http://localhost:8000/product/1

# Create new product
curl -X POST "http://localhost:8000/product/create/" \
  -H "X-API-KEY: your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Product", "price": 29.99, "in_stock": true}'

# Update product
curl -X PUT "http://localhost:8000/product/update/1" \
  -H "X-API-KEY: your_secret_key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Product", "price": 39.99, "in_stock": false}'

# Delete product
curl -X DELETE "http://localhost:8000/product/remove/1" \
  -H "X-API-KEY: your_secret_key"
```

### Using Python requests

```python
import requests

headers = {"X-API-KEY": "your_secret_key"}

# Get all products
response = requests.get("http://localhost:8000/product/all", headers=headers)
print(response.json())

# Create new product
product_data = {
    "name": "Test Product",
    "price": 19.99,
    "in_stock": True,
    "discount": 0.1
}
response = requests.post("http://localhost:8000/product/create/", 
                        json=product_data, headers=headers)
print(response.json())
```

## Recent Updates

### Security Implementation

- Added API key authentication for protected endpoints
- Implemented `security.py` module with reusable security functions
- Environment variable management with `.env` files
- Proper HTTP 403 error responses for unauthorized access

### Enhanced CRUD Operations

- Complete CRUD functionality (Create, Read, Update, Delete)
- Advanced Pydantic validation with field constraints
- Optional fields support (discount field)
- Improved error handling and status codes

### Code Organization

- Modular architecture with separate security layer
- Dependency injection for shared logic and security
- Environment configuration with `.env.example` template
- Updated `.gitignore` to allow `.env.example` while protecting `.env`

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

- Ensure `.env` file is in the project root directory
- Verify API key format in `.env`: `API_KEY=your_secret_key` (no quotes)
- Check that `python-dotenv` is installed
- Restart server after modifying `.env` file

### Validation Errors

- Product name must be 2-12 characters long
- Price must be greater than 1
- Check field names match model exactly
- Ensure JSON content-type header for POST/PUT requests

---

*This project serves as a foundation for understanding FastAPI fundamentals and common API development patterns.*clear
