from fastapi import FastAPI
from app.routers import fondo

app = FastAPI()

@app.get("/",tags=["Bienvenida"])
def bienvenido():
    return {"Mensaje":"Bienvenido a la API de BTG Pactual"}


app.include_router(fondo.router)