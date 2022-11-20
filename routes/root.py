from fastapi import APIRouter
import uvicorn

root = APIRouter()


@root.get("/")
async def index():
    return {"message": "Hi!"}
