from fastapi import APIRouter
from models.userModel import User,UserLogin
from pymongo import MongoClient
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, UploadFile, File
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()

client = MongoClient("mongodb://localhost:27017/")
db = client["universityApi"]
users_collection = db["users"]

def get_user(email: str):
    user = users_collection.find_one({"email": email})
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup")
def register(user: User):
    existing_user = get_user(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    users_collection.insert_one(user.dict())
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    existing_user = get_user(user.email)
    if not existing_user:
        raise HTTPException(status_code=403, detail="Invalid email")
    
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=403, detail="Invalid password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": existing_user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

