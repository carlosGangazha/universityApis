from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float
    payment_method: str
    picture: str
