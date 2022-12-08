import requests
from dotenv import load_dotenv, dotenv_values
from models.events import Alamat

load_dotenv()
config = dotenv_values(".env")

api_key = config["API_KEY"]

class mapsapi():
    def getDrivingDistanceMaps(self, origin: Alamat, destination: Alamat):

        alamatOrigin = origin.jalan + origin.kota
        alamatDestination = destination.jalan + destination.kota

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={alamatOrigin}&destinations={alamatDestination}&key={api_key}"

        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response

class daveroot():
    def getDaveRoot(self):

        url = "http://128.199.149.182:8001"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response


