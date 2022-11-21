from fastapi import APIRouter
import uvicorn

routes_root = APIRouter()


@routes_root.get("/")
async def index():
    return {"message": "Hi!"}
