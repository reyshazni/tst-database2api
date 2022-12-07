from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.events import Alamat, UpdateBensin
from services.auth import AuthHandler, JWTBearer
from services.database_manager import dbInstance
from services.maps import mapsapi
from sqlalchemy import text

event_router = APIRouter(
    tags=["Events"]
)

@event_router.get("/get-all-bensin")
def getAllBensin(Authorize: JWTBearer = Depends(JWTBearer())):
    pertamaxO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertamax"})
    pertaliteO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"pertalite"})
    solarO = dbInstance.conn.execute(text("SELECT harga FROM bensin WHERE jenisBensin=:jenisBensin") , {"jenisBensin":"solar"})
    
    for getterPertamax in pertamaxO:
        hargaPertamax = getterPertamax[0]
        
    for getterPertalite in pertaliteO:
        hargaPertalite = getterPertalite[0]

    for getterSolar in solarO:
        hargaSolar = getterSolar[0]
    
    return {"Pertamax": hargaPertamax, "Pertalite": hargaPertalite, "solar": hargaSolar}

@event_router.get("/get-avg-bensin")
def getAverageBensin():
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
    
@event_router.put('/update-bensin', status_code=201)
def updateBensin(updateBensinParam: UpdateBensin, Authorize: JWTBearer = Depends(JWTBearer())):
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

@event_router.get("/get-alamat-counter")
def getAlamatCounter(Authorize: JWTBearer = Depends(JWTBearer())):
    jalanO = dbInstance.conn.execute(text("SELECT jalan FROM alamat"))
    kotaO = dbInstance.conn.execute(text("SELECT kota FROM alamat"))
    for getterJalan in jalanO:
        jalanCounter = getterJalan[0]
        
    for getterKota in kotaO:
        kotaCounter = getterKota[0]

    alamatCounter = (jalanCounter + " " + kotaCounter)
    
    return {"alamatCounter": alamatCounter}

@event_router.put('/update-alamat-counter', status_code=201)
def updateBensin(updateAlamatParam: Alamat, Authorize: JWTBearer = Depends(JWTBearer())):

    newBensin = {"jalan": updateAlamatParam.jalan.lower(), "kota": updateAlamatParam.kota.lower()}

    query = text("UPDATE alamat SET jalan = :jalan, kota = :kota")

    try:
        dbInstance.conn.execute(query, newBensin)
        return {"message": "alamat Berhasil diperbarui!"}
    except:
        raise HTTPException(status_code=406, detail="Update gagal, silakan coba lagi!")

@event_router.post("/get-price")
def getPrice(originParam: Alamat, destinationParam: Alamat):
    drivingDist = mapsapi()
    msg = drivingDist.getDrivingDistanceMaps(originParam, destinationParam)

    distance = msg["rows"][0]["elements"][0]["distance"]["value"]
    seconds = msg["rows"][0]["elements"][0]["duration"]["value"]

    avg_speed = distance/seconds

    avg_speed_kmh = avg_speed * 3.6

    if avg_speed <= 3:
        eta = 1.5
    elif avg_speed <= 5:
        eta = 1.2
    else:
        eta = 1

    basicPrice = 4*(distance/3)
    
    efficiency = 40000
    hargaBensin = int(getAverageBensin()["Harga rata-rata bensin"])
    price = ((distance*hargaBensin*eta)/efficiency) + basicPrice
    return {"origin": msg["origin_addresses"][0],
            "destination": msg["destination_addresses"][0],
            "drivingDistance": distance,
            "drivingTime": seconds,
            "avgSpeed": avg_speed_kmh,
            "price": price
    }