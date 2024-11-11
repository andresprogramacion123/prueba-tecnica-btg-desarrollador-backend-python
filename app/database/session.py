from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

MONGO_DETAILS = "mongodb://mongodb:27017"
#MONGO_DETAILS = "mongodb://localhost:27017" # Para ejecucion sin docker

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.btg_db

fondos_db = [
    {"_id": "1", "nombre": "FPV_BTG_PACTUAL_RECAUDADORA", "monto_minimo": 75000,"categoria": "FPV"},
    {"_id": "2", "nombre": "FPV_BTG_PACTUAL_ECOPETROL", "monto_minimo": 125000, "categoria": "FPV"},
    {"_id": "3", "nombre": "DEUDAPRIVADA", "monto_minimo": 50000, "categoria": "FIC"},
    {"_id": "4", "nombre": "FDO-ACCIONES", "monto_minimo": 250000, "categoria": "FIC"},
    {"_id": "5", "nombre": "FPV_BTG_PACTUAL_DINAMICA", "monto_minimo": 100000, "categoria": "FPV"}
]

usuarios_db=[
    {
        "_id": "1",
        "nombre": "julian",
        "correo": "julian@gmail.com",
        "telefono": 3005444343,
        "saldo_disponible": 500000,
        "saldo_fondos": [0,0,0,0,0],
        "transacciones": []
    }
]

async def insertar_datos():
    try:
        #colección "fondos"
        coleccion_fondos = db.fondos
        #colección "usuarios"
        coleccion_usuarios = db.usuarios
        result_fondos = await coleccion_fondos.insert_many(fondos_db)
        result_usuarios = await coleccion_usuarios.insert_many(usuarios_db)
        print("Documentos insertados")
    except Exception as e:
        print("Error al insertar documentos:", e)

# Ejecuta la función asincrónica
if __name__ == "__main__":
    asyncio.run(insertar_datos())