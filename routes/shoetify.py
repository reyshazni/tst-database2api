from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, status
from models.events import Alamat, UpdateBensin
from routes.events import getAverageBensin
from services.auth import AuthHandler, JWTBearer
from services.database_manager import dbInstance
from services.urlhandler import mapsapi, daveroot
from sqlalchemy import text


shoetify_router = FastAPI(openapi_prefix="/shoetify")

@shoetify_router.post("/order")
def getPrice(alamatAwal: Alamat, alamatTujuan: Alamat):
    drivingDist = mapsapi()
    msg = drivingDist.getDrivingDistanceMaps(alamatAwal, alamatTujuan)

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
            "drivingDistanceMeter": distance,
            "drivingTimeSeconds": seconds,
            "avgSpeedKmh": avg_speed_kmh,
            "priceRupiah": price
    }