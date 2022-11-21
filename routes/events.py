from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status

event_router = APIRouter(
    tags=["Events"]
)

@event_router.get("/")
async def index():
    return {"message": "Hi, this is event 1!"}