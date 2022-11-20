from fastapi import FastAPI
import uvicorn
import models.distance
import routes.root

app = FastAPI()

app.include_router(routes.root.root)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000,
                log_level="info", reload=True)
