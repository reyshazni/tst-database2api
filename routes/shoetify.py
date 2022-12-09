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

    distance1 = msg["rows"][0]["elements"][0]["distance"]["value"]
    seconds1 = msg["rows"][0]["elements"][0]["duration"]["value"]

    distance2 = msg2["rows"][0]["elements"][0]["distance"]["value"]
    seconds2 = msg2["rows"][0]["elements"][0]["duration"]["value"]

    avg_speed1 = distance1/seconds1

    avg_speed2 = distance2/seconds2

    avg_speed_kmh1 = avg_speed1 * 3.6

    avg_speed_kmh2 = avg_speed2 * 3.6

    if avg_speed1 <= 3:
        eta1 = 1.5
    elif avg_speed1 <= 5:
        eta1 = 1.2
    else:
        eta1 = 1

    if avg_speed2 <= 3:
        eta2 = 1.5
    elif avg_speed2 <= 5:
        eta2 = 1.2
    else:
        eta2 = 1

    basicPrice1 = 4*(distance1/3) + 4000
    basicPrice2 = 4*(distance2/3) + 4000
    
    efficiency = 40000
    hargaBensin = int(getAverageBensin()["Harga rata-rata bensin"])
    price1 = ((distance1*hargaBensin*eta1)/efficiency) + basicPrice1
    price2 = ((distance2*hargaBensin*eta2)/efficiency) + basicPrice2
    
    newOrder = {"namaPengambil": alamatAwal.nama, "namaPenerima": alamatTujuan.nama, "jalanAwal": alamatAwal.jalan, "kotaAwal": alamatAwal.kota, "jalanTujuan": alamatTujuan.jalan, "kotaTujuan": alamatTujuan.kota, "price1": price1, "price2": price2}

    query = text("INSERT INTO orderkurirku (namaPengambil, namaPenerima, jalanAwal, kotaAwal, jalanTujuan, kotaTujuan, price) VALUES (:namaPengambil, :namaPenerima, :jalanAwal, :kotaAwal, :jalanTujuan, :kotaTujuan, :price1)")
    query2 = text("INSERT INTO orderkurirku (namaPenerima, namaPengambil, jalanTujuan, kotaTujuan, jalanAwal, kotaAwal, price) VALUES (:namaPengambil, :namaPenerima, :jalanAwal, :kotaAwal, :jalanTujuan, :kotaTujuan, :price2)")
    try:
        dbInstance.conn.execute(query, newOrder)
        dbInstance.conn.execute(query2, newOrder)
        return {"origin": msg["origin_addresses"][0],
            "destination": msg["destination_addresses"][0],
            "drivingDistanceMeters": distance1,
            "drivingTimeSeconds": seconds1,
            "avgSpeedKmh": avg_speed_kmh1,
            "priceRupiah": price1,
            "message": "order berhasil dibuat!"
    }
    except:
        raise HTTPException(status_code=406, detail="Order gagal, silakan coba lagi")