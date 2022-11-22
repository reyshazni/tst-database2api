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

