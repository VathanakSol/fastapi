from pydantic import BaseModel, Field
from typing import Optional

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
    4: {
        "name": "Product 4",
        "price": 59.99,
        "in_stock": True
    },
}