from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True

# Dictionary for fake database
Inventory = {
    1: {
        "name": "Product 1",
        "price": 24.99,
        "in_stock": True
    },
    2: {
        "name": "Product 2",
        "price": 19.99,
        "in_stock": False
    },
    3: {
        "name": "Product 3",
        "price": 14.99,
        "in_stock": True
    },
}