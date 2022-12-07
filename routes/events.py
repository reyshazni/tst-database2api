from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.events import Distance
from services.auth import AuthHandler, JWTBearer
from services.database_manager import dbInstance
from sqlalchemy import text

event_router = APIRouter(
    tags=["Events"]
)

@event_router.post("/distance/")
async def getjarak(distance: Distance):
    jarak = distance.getDistance(distance.alamat1, distance.alamat2)
    return {"Alamat": distance,
            "Jarak": jarak}

@event_router.get("/get-all-bensin/")
async def getAllBensin(Authorize: JWTBearer = Depends(JWTBearer())):
    pertamaxO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertamax"})
    pertaliteO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertalite"})
    solarO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"solar"})
    hargaPertamax = 0
    hargaPertalite = 0
    hargaSolar = 0
    for getterPertamax in pertamaxO:
        hargaPertamax = getterPertamax[0]
        
    for getterPertalite in pertaliteO:
        hargaPertalite = getterPertalite[0]

    for getterSolar in solarO:
        hargaSolar = getterSolar[0]
    
    return {"Pertamax": hargaPertamax, "Pertalite": hargaPertalite, "solar": hargaSolar}

@event_router.get("/get-avg-bensin/")
async def getAllBensin(Authorize: JWTBearer = Depends(JWTBearer())):
    pertamaxO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertamax"})
    pertaliteO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertalite"})
    solarO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"solar"})
    
    hargaPertamax = 0
    hargaPertalite = 0
    hargaSolar = 0

    weighterPertamax = 2
    weighterPertalite = 5
    weighterSolar = 1
    weighterTotal = weighterPertamax + weighterPertalite + weighterSolar

    for getterPertamax in pertamaxO:
        hargaPertamax = getterPertamax[0]
        
    for getterPertalite in pertaliteO:
        hargaPertalite = getterPertalite[0]

    for getterSolar in solarO:
        hargaSolar = getterSolar[0]

    hargaAverage = ((hargaPertamax*weighterPertamax) + (hargaPertalite*weighterPertalite) + (hargaSolar*weighterSolar))/weighterTotal
    
    return {"Harga rata-rata bensin": hargaAverage}
    