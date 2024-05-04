from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, File
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

class User(BaseModel):
    reg_number:str
    fullname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str