from models.productsModel import Product
from fastapi import APIRouter
from pymongo import MongoClient
from fastapi import HTTPException,File,UploadFile


p_router = APIRouter()


client = MongoClient("mongodb://localhost:27017/")
db = client["universityApi"]
products_collection = db["products"]

@p_router.post("/addProduct")
async def create_product(product: Product):
    picture_data = product.picture
    product_data = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "payment_method": product.payment_method,
        "picture": picture_data
    }
    inserted_product = products_collection.insert_one(product_data)
    return {"message": "Product created successfully"}

@p_router.get("/getAllProducts")
async def get_all_products():
    products = list(products_collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return products


@p_router.delete("/deleteProduct/{product_name}")
async def delete_product_by_name(product_name: str):
    existing_product = products_collection.find_one({"name": product_name})
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    result = products_collection.delete_one({"name": product_name})

    return {"message": "Product deleted successfully"}