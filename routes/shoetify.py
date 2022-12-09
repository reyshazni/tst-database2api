from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, status
from models.events import Alamat, UpdateBensin
from routes.events import getAverageBensin
from services.auth import AuthHandler, JWTBearer
from services.database_manager import dbInstance
from services.urlhandler import mapsapi, daveroot
from sqlalchemy import text

shoetify = FastAPI()

def getNamaNotelp():
    nama = "dave"
    notelp = "088216734613"
    return {"nama": nama,
            "notelp": notelp}

@shoetify.post("/order-shoetify")
def getPriceDave(alamatAwal: Alamat, alamatTujuan: Alamat):
    drivingDist = mapsapi()
    msg = drivingDist.getDrivingDistanceMaps(alamatAwal, alamatTujuan)
    msg2 = drivingDist.getDrivingDistanceMaps(alamatTujuan, alamatAwal)

    distance = msg["rows"][0]["elements"][0]["distance"]["value"] + msg2["rows"][0]["elements"][0]["distance"]["value"]
    seconds = msg["rows"][0]["elements"][0]["duration"]["value"] + msg2["rows"][0]["elements"][0]["duration"]["value"]

    fromDave = getNamaNotelp()

    nama = fromDave["nama"]
    notelp = fromDave["notelp"]

    avg_speed = distance/seconds

    avg_speed_kmh = avg_speed * 3.6

    if avg_speed <= 3:
        eta = 1.5
    elif avg_speed <= 5:
        eta = 1.2
    else:
        eta = 1

    basicPrice = 4*(distance/3) + 4000
    
    efficiency = 40000
    hargaBensin = int(getAverageBensin()["Harga rata-rata bensin"])
    price = ((distance*hargaBensin*eta)/efficiency) + basicPrice

    newOrder = {"nama": nama, "notelp": notelp, "jalanAwal": alamatAwal.jalan, "kotaAwal": alamatAwal.kota, "jalanTujuan": alamatTujuan.jalan, "kotaTujuan": alamatTujuan.kota, "price": price}

    query = text("INSERT INTO orderkurirku (nama, notelp, jalanAwal, kotaAwal, jalanTujuan, kotaTujuan, price) VALUES (:nama, :notelp, :jalanAwal, :kotaAwal, :jalanTujuan, :kotaTujuan, :price)")
    query2 = text("INSERT INTO orderkurirku (nama, notelp, jalanAwal, kotaAwal, jalanTujuan, kotaTujuan, price) VALUES (:nama, :notelp, :jalanTujuan, :kotaTujuan, :jalanTujuan, :kotaAwal, :price)")
    try:
        dbInstance.conn.execute(query, newOrder)
        dbInstance.conn.execute(query2, newOrder)
        return {"origin": msg["origin_addresses"][0],
            "destination": msg["destination_addresses"][0],
            "drivingDistanceMeters": distance,
            "drivingTimeSeconds": seconds,
            "avgSpeedKmh": avg_speed_kmh,
            "priceRupiah": price,
            "msg": "order berhasil dibuat!"
    }
    except:
        raise HTTPException(status_code=406, detail="Order gagal, silakan coba lagi")