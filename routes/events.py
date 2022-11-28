from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.events import Distance
from services.auth import AuthHandler, JWTBearer

event_router = APIRouter(
    tags=["Events"]
)

@event_router.post("/distance/")
async def getjarak(distance: Distance):
    jarak = distance.getDistance(distance.alamat1, distance.alamat2)
    return {"Alamat": distance,
            "Jarak": jarak}
    
@event_router.post("/protected/")
async def testprotect(Authorize: JWTBearer = Depends(JWTBearer())):
    return {"message": "you are logged in", "msg":Authorize}
