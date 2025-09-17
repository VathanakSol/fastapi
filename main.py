from fastapi import FastAPI, HTTPException

from product import Product, Inventory

app = FastAPI()

# Testing Hello World
@app.get("/")
def root():
    return {
        "message":"Hello FastAPI3"
    }

# Get Message  
@app.get("/testing")
def testing():
    return {
        "display":"this is a message"
    }

# Get Product Name
@app.get("/product/name/{product_name}")
def product(product_name: str):
    return {
        "product": product_name
    }

# Get All Products from fake database
@app.get("/product/all")
def get_all_product():
    return Inventory

# Get Product via ID
@app.get("/product/{item_id}")
def get_product_id(item_id: int):
    if item_id not in Inventory: 
        raise HTTPException(status_code=404, detail="Product Not Found")
    return Inventory[item_id]

# Add New Product
@app.post("/product/create/")
def create_product(item: Product):

    new_id = max(Inventory.keys()) + 1 if Inventory else 1
    Inventory[new_id] = item.dict()

    return {
        "status": "Product added successfully",
        "product_id": new_id,
        "product": Inventory[new_id]
    }

# Update Product via ID
@app.put("/product/update/{item_id}")
def update_product(item_id: int, product: Product):
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
def remove_product(item_id: int):
    if item_id not in Inventory:
        raise HTTPException(status_code=404, detail="Product Not Found")

    removed_product = Inventory.pop(item_id)

    return {
        "status": "Deleted product successfully",
        "product_id": item_id,
        "deleted_product": removed_product,
    }


