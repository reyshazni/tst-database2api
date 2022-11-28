from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from routes.events import event_router
from routes.users import user_router

app = FastAPI()

app.include_router(event_router, prefix="/event")
app.include_router(user_router, prefix="/user")

@app.get("/")
async def home():
    return {"message": "Welcome to Rey's API!"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")
