from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends, HTTPException, Request, status
from models.events import Distance
from geopy.geocoders import Nominatim
import geopy.distance

event_router = APIRouter(
    tags=["Events"]
)

@event_router.post("/distance/")
async def getjarak(distance: Distance):
    jarak = getDistance(distance.alamat1, distance.alamat2)
    return {"Alamat": distance,
            "Jarak": jarak}




def getLatLon(alamat):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(alamat)
    locArray = [location.latitude, location.longitude]
    return locArray

def getDistance(alamatToko, alamatCust):
    coords_1 = (getLatLon(alamatToko)[0], getLatLon(alamatToko)[1])
    coords_2 = (getLatLon(alamatCust)[0], getLatLon(alamatCust)[1])
    return geopy.distance.geodesic(coords_1, coords_2).km