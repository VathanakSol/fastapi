from fastapi import APIRouter, Depends, HTTPException
from config.security import get_api_key
from database import Inventory
from schemas.product import Product

router = APIRouter(prefix="/api/v1/product", tags=["Products"])

# Get All Product
@router.get("/")
def get_all_product(api_key: str = Depends(get_api_key)):
    return Inventory

# Get Product via ID
@router.get("/{item_id}")
def get_product_id(item_id: int, api_key: str = Depends(get_api_key)):
    if item_id not in Inventory: 
        raise HTTPException(status_code=404, detail="Product Not Found")
    return Inventory[item_id]


# Add New Product
@router.post("/create")
def create_product(item: Product, api_key: str = Depends(get_api_key)):

    new_id = max(Inventory.keys()) + 1 if Inventory else 1
    Inventory[new_id] = item.dict()

    return {
        "status": "Product added successfully",
        "product_id": new_id,
        "product": Inventory[new_id]
    }


# Update Product via ID
@router.put("/product/update/{item_id}")
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
@router.delete("/product/remove/{item_id}")
def remove_product(item_id: int, api_key: str = Depends(get_api_key)):
    if item_id not in Inventory:
        raise HTTPException(status_code=404, detail="Product Not Found")

    removed_product = Inventory.pop(item_id)

    return {
        "status": "Deleted product successfully",
        "product_id": item_id,
        "deleted_product": removed_product,
    }