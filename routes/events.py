from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.events import Distance

event_router = APIRouter(
    tags=["Events"]
)

@event_router.get("/distance/")
async def getjarak(distance: Distance):
    return distance
