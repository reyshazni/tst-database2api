from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.events import Distance, updateBensin
from services.auth import AuthHandler, JWTBearer
from services.database_manager import dbInstance
from sqlalchemy import text

event_router = APIRouter(
    tags=["Events"]
)

@event_router.post("/distance")
async def getjarak(distance: Distance):
    jarak = distance.getDistance(distance.alamat1, distance.alamat2)
    return {"Alamat": distance,
            "Jarak": jarak}

@event_router.get("/get-all-bensin")
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

@event_router.get("/get-avg-bensin")
async def getAverageBensin(Authorize: JWTBearer = Depends(JWTBearer())):
    pertamaxO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertamax"})
    pertaliteO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertalite"})
    solarO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"solar"})

    ## Tambahkan weighter menyesuaikan dengan jumlah pengguna jenis bensin
    weighterPertamax = 2
    weighterPertalite = 6
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
    
@event_router.put('/change-bensin', status_code=201)
def updateBensin(updateBensinParam: updateBensin):
    listJenisBensin = ['pertamax', 'pertalite', 'solar']
    
    if (updateBensinParam.hargaBaru < 1000):
        raise HTTPException(status_code=405, detail="Masukkan harga baru dengan benar!")
        return
    
    if (updateBensinParam.jenisBensin.lower() not in listJenisBensin):
        raise HTTPException(status_code=405, detail="Jenis bensin tidak terdaftar!")
        return

    newBensin = {"jenisBensin": updateBensinParam.jenisBensin.lower(), "hargaBaru": updateBensinParam.hargaBaru}

    query = text("UPDATE bensin SET jenisBensin = :jenisBensin, harga = :hargaBaru WHERE jenisBensin = :jenisBensin")

    try:
        dbInstance.conn.execute(query, newBensin)
        return {"message": "Harga Berhasil diperbarui!"}
    except:
        raise HTTPException(status_code=406, detail="Update gagal, silakan coba lagi!")