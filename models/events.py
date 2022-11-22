from fastapi import FastAPI
from pydantic import BaseModel
from geopy.geocoders import Nominatim
import geopy.distance

class Distance(BaseModel):
    alamat1: str
    alamat2: str
    
    def getLatLon(alamat):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(alamat)
    locArray = [location.latitude, location.longitude]
    return locArray

    def getDistance(alamatToko, alamatCust):
        coords_1 = (getLatLon(alamatToko)[0], getLatLon(alamatToko)[1])
        coords_2 = (getLatLon(alamatCust)[0], getLatLon(alamatCust)[1])
        return geopy.distance.geodesic(coords_1, coords_2).km

