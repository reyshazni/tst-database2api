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

    def getDistance(self, alamatToko, alamatCust):
        coords_1 = (self.getLatLon(alamatToko)[0], self.getLatLon(alamatToko)[1])
        coords_2 = (self.getLatLon(alamatCust)[0], self.getLatLon(alamatCust)[1])
        return geopy.distance.geodesic(coords_1, coords_2).km
    
    class Config:
        schema_extra = {
            "example": {
                "alamat1": "Dago Asri Bandung",
                "alamat2": "Taman Setiabudi Semarang"
            }
        }

class Bensin(BaseModel):
    pertamax: int
    pertalite: int
    solar: int

    class Config:
        schema_extra = {
            "example": {
                "pertamax": "10000",
                "pertalite": "8000",
                "solar": "6000"
            }
        }

class updateBensin(BaseModel):
    jenisBensin: str
    hargaBaru: int

    class Config:
        schema_extra = {
            "example": {
                "jenisBensin": "pertamax",
                "hargaBaru": "16000"
            }
        }