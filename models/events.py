from fastapi import FastAPI
from pydantic import BaseModel

class Distance(BaseModel):
    alamat1: str
    alamat2: str

