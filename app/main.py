from fastapi import FastAPI
from app.routers import fondo

app = FastAPI()

app.include_router(fondo.router)