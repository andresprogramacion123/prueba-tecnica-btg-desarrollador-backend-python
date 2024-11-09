from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.btg_db

fondos_db = [
    {"_id": "1", "nombre": "FPV_BTG_PACTUAL_RECAUDADORA", "monto_minimo": 75000,"categoria": "FPV"},
    {"_id": "2", "nombre": "FPV_BTG_PACTUAL_ECOPETROL", "monto_minimo": 125000, "categoria": "FPV"},
    {"_id": "3", "nombre": "DEUDAPRIVADA", "monto_minimo": 50000, "categoria": "FIC"},
    {"_id": "4", "nombre": "FDO-ACCIONES", "monto_minimo": 250000, "categoria": "FIC"},
    {"_id": "5", "nombre": "FPV_BTG_PACTUAL_DINAMICA", "monto_minimo": 100000, "categoria": "FPV"}
]

async def insertar_fondos():
    try:
        # Obtén la colección "fondos"
        coleccion_fondos = db.fondos
        # Inserta los documentos
        result = await coleccion_fondos.insert_many(fondos_db)
        print("Documentos insertados con los IDs:", result.inserted_ids)
    except Exception as e:
        print("Error al insertar documentos:", e)

# Ejecuta la función asincrónica
if __name__ == "__main__":
    asyncio.run(insertar_fondos())