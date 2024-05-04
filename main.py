from fastapi import FastAPI
from pymongo import MongoClient
import base64
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from routers.users import router as user_router
from routers.products import p_router as product_router
from routers.business import b_router as business_router

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]
products_collection = db["products"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(product_router)
app.include_router(business_router)


@app.get("/hello")
def hello():
    return{"hello":"world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)