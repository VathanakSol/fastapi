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

# Get Product Id
# @app.get("/product/id/{product_id}")
# def product_id(product_id: int):
#     return {
#         "product_id": product_id,
#     }

# Get Product Id with Detail Query Parameter 
# @app.get("/product/{product_id}")
# def product_detail(product_id: int, detail: str | None = None):
#     return {
#         "product_id": product_id,
#         "detail": detail
#     }

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

# # Create Product
# @app.post("/product/create/")
# def create_product(product: Product):
#     return {
#         "status":"Product has created",
#         "Product": product  
#     }

# Update existing product
# @app.put("/product/{product_id}")
# def update_product(product_id: int, product: Product ):
#     return {
#         "status":"product has updated",
#         "product_id": product_id,
#         "product_updated": product
#     }


