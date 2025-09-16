# FastAPI Product Management API

A simple REST API built with FastAPI for managing products. This project demonstrates core FastAPI concepts, common error handling, and API design patterns.

## Project Structure

```
├── main.py          # Main FastAPI application with route definitions
├── product.py       # Pydantic models and data storage
└── README.md        # Project documentation
```

## Key Files

### `main.py`
- Contains the FastAPI application instance
- Defines all API endpoints (routes)
- Handles HTTP methods: GET, POST, PUT
- Implements error handling with HTTPException

### `product.py`
- Defines the `Product` Pydantic model for data validation
- Contains the `Inventory` dictionary (fake database)
- Provides data structure for the API

## API Endpoints

### Basic Endpoints
- `GET /` - Hello World message
- `GET /testing` - Test endpoint

### Product Endpoints
- `GET /product/name/{product_name}` - Get product by name
- `GET /product/all` - Get all products from inventory
- `GET /product/{item_id}` - Get specific product by ID
- `POST /product/create/` - Create new product (commented out)
- `PUT /product/{product_id}` - Update existing product (commented out)

## Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Interactive Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Concepts Learned

### 1. Pydantic Models
```python
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True
```
- Provides automatic data validation
- Converts JSON to Python objects
- Generates API documentation automatically

### 2. Route Parameters
```python
@app.get("/product/{item_id}")
def get_product_id(item_id: int):
```
- `{item_id}` captures URL path parameters
- FastAPI automatically converts types (string to int)
- Type hints provide validation

### 3. Error Handling
```python
if item_id not in Inventory: 
    raise HTTPException(status_code=404, detail="Product Not Found")
```
- Use `HTTPException` for proper HTTP error responses
- Common status codes: 404 (Not Found), 422 (Unprocessable Entity)

## Common Errors and Solutions

### 422 Unprocessable Entity
**Cause**: Data validation failed
**Solutions**:
- Check field names match between Pydantic model and data
- Ensure correct data types
- Verify required fields are provided

**Example**: Model expects `in_stock` but data has `stock`

### Route Conflicts
**Problem**: `/product/all` conflicts with `/product/{product_id}`
**Solution**: Put specific routes before generic ones

```python
# ✅ Correct order
@app.get("/product/all")      # Specific route first
@app.get("/product/{item_id}") # Generic route second

# ❌ Wrong order
@app.get("/product/{item_id}") # Generic catches everything
@app.get("/product/all")       # Never reached
```

### Import Errors
**Problem**: `ImportError` when importing from modules
**Solution**: Ensure exact naming matches

```python
# In product.py
Inventory = {...}

# In main.py
from product import Inventory  # Must match exactly
```

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
# Get all products
curl http://localhost:8000/product/all

# Get specific product
curl http://localhost:8000/product/1

# Test error handling
curl http://localhost:8000/product/999
```

### Using Python requests
```python
import requests

# Get all products
response = requests.get("http://localhost:8000/product/all")
print(response.json())

# Get specific product
response = requests.get("http://localhost:8000/product/1")
print(response.json())
```

## Next Steps for Enhancement

1. **Database Integration**: Replace dictionary with SQLAlchemy/databases
2. **Authentication**: Add JWT token authentication
3. **Validation**: Add more complex validation rules
4. **Testing**: Add unit tests with pytest
5. **Deployment**: Configure for production deployment
6. **Logging**: Add proper logging for debugging
7. **CORS**: Configure CORS for frontend integration

## Troubleshooting

### Server Won't Start
- Check for syntax errors in Python files
- Ensure all imports are correct
- Verify FastAPI and uvicorn are installed

### 422 Errors
- Check Pydantic model matches your data structure
- Verify field names are identical
- Ensure data types match model expectations

### Route Not Found
- Check route order (specific before generic)
- Verify URL path matches route definition
- Check for typos in route paths

---

*This project serves as a foundation for understanding FastAPI fundamentals and common API development patterns.*clear
