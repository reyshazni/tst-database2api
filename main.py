from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import models.distance
from routes.events import event_router

app = FastAPI()

app.include_router(event_router, prefix="/event")

@app.get("/")
async def home():
    return {"message": "Welcome to Rey's API!"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000,
                log_level="info", reload = True)
