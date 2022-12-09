from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from routes.events import event_router, getAverageBensin
from routes.users import user_router
from routes.shoetify import shoetify_router
import services.database_manager
from services.urlhandler import mapsapi
from models.events import Alamat
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()
shoetify = FastAPI()

app.include_router(event_router, prefix="/event")
app.include_router(user_router, prefix="/user")
app.include_router(shoetify_router, prefix="/shoetify")

@app.get("/")
async def home():
    return {"message": "Welcome to Rey's API!"}

shoetify.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["128.199.149.182"] 
)

@shoetify.post("/order")
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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")

