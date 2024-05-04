from models.businessModel import Bussiness
from pymongo import MongoClient
from fastapi import APIRouter

b_router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client["universityApi"]
profiles_collection = db["businessProfiles"]

@b_router.post("/createBusinessProf")
async def create_profile(business:Bussiness):
    await profiles_collection.insert_one(business.dict())

    return {"message": "Business profile created successfully"}