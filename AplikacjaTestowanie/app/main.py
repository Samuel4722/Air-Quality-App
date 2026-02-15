from fastapi import FastAPI
from app.routers.air_quality import router

app = FastAPI(title="Air Quality App")

app.include_router(router)
