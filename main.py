from fastapi import FastAPI, HTTPException, Depends

import os

from dotenv import load_dotenv

from product import Product, Inventory
from security import get_api_key

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()

# View Information With Security 
@app.get("/views/secure/")
def secure_data(api_key: str = Depends(get_api_key)):
    return {
        "status": "You have access ✅",
        "api_key": api_key
    }

# Shared Logic
def common_parameters(q: str | None = None, limit: int = 10):
    return {
        "q": q,
        "limit": limit
    }


# Use Shared Logic
@app.get("/views/")
def view_products(commons: dict = Depends(common_parameters)):
    return commons

# Get Information With Security Mode
@app.get("/info")
def testing(api_key: str = Depends(get_api_key)):
    return {
        "display": "Product Testing"
    }

# Get Product Name
@app.get("/product/name/{product_name}")
def product(product_name: str):
    return {
        "product": product_name
    }

# Get All Products from fake database
@app.get("/product/all")
def get_all_product(api_key: str = Depends(get_api_key)):
    return Inventory

# Get Product via ID
@app.get("/product/{item_id}")
def get_product_id(item_id: int, api_key: str = Depends(get_api_key)):
    if item_id not in Inventory: 
        raise HTTPException(status_code=404, detail="Product Not Found")
    return Inventory[item_id]

# Add New Product
@app.post("/product/create/")
def create_product(item: Product, api_key: str = Depends(get_api_key)):

    new_id = max(Inventory.keys()) + 1 if Inventory else 1
    Inventory[new_id] = item.dict()

    return {
        "status": "Product added successfully",
        "product_id": new_id,
        "product": Inventory[new_id]
    }

# Update Product via ID
@app.put("/product/update/{item_id}")
def update_product(item_id: int, product: Product, api_key: str = Depends(get_api_key)):
    if item_id not in Inventory:
        raise HTTPException(status_code=404, detail="Product Not Found")
    
    Inventory[item_id] = product.dict()

    return {
        "status": "Product updated successfully",
        "product_id": item_id,
        "product": Inventory[item_id],
    }

# Delete Product via ID
@app.delete("/product/remove/{item_id}")
def remove_product(item_id: int, api_key: str = Depends(get_api_key)):
    if item_id not in Inventory:
        raise HTTPException(status_code=404, detail="Product Not Found")

    removed_product = Inventory.pop(item_id)

    return {
        "status": "Deleted product successfully",
        "product_id": item_id,
        "deleted_product": removed_product,
    }


