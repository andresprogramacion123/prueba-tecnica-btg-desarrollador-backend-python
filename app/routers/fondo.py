from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.fondo import Fondo, Usuario
from app.database.session import db
import uuid
from datetime import datetime
from enum import Enum

router = APIRouter()

@router.get("/hola")
def hola_mundo():
    return {"Hola":"Mundo"}

class TipoNotificacion(str, Enum):
    email = "email"
    sms = "sms"

#Ver todos los fondos
@router.get("/fondos/", response_model=List[Fondo], tags=["Fondos"])
async def obtener_fondos():
    fondos = await db.fondos.find().to_list(1000)
    return [Fondo(**fondo) for fondo in fondos]

#Suscribirse a un nuevo fondo
@router.post("/usuarios/{usuario_id}/suscribir/{fondo_id}/vinculacion/{valor_vinculacion}", tags=["Negocio"])
async def suscribir_fondo(usuario_id: str, fondo_id: str, valor_vinculacion: float, notificacion: TipoNotificacion):
    usuario = await db.usuarios.find_one({"_id": usuario_id})
    fondo = await db.fondos.find_one({"_id": fondo_id})

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not fondo:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")
    
    if valor_vinculacion > usuario['saldo_disponible']:
        raise HTTPException(status_code=400, detail=f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}. Intente con otro valor")

    if valor_vinculacion < fondo['monto_minimo']:
        raise HTTPException(status_code=400, detail=f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}")
    
    # Deduce el saldo y registra la transacción
    usuario['saldo_disponible'] = usuario['saldo_disponible'] - valor_vinculacion
    usuario['saldo_fondos'][int(fondo_id)-1]= valor_vinculacion + usuario['saldo_fondos'][int(fondo_id)-1]
    usuario['transacciones'].append({
        "id": str(uuid.uuid4()),
        "id_fondo": fondo_id,
        "nombre_fondo": fondo['nombre'],
        "valor": valor_vinculacion,
        "tipo_transaccion": "apertura",
        "fecha": datetime.now().isoformat()  # Agrega la fecha actual en formato ISO
    })
    await db.usuarios.replace_one({"_id": usuario_id}, usuario)

    if notificacion == "sms":
        mensaje= f"Suscripción exitosa, se envio mensaje de texto al telefono {usuario['telefono']}"
    else:
        mensaje= f"Suscripción exitosa, se envio email al correo {usuario['correo']}"
    return {"mensaje": mensaje, "saldo_actual": usuario['saldo_disponible']}

#Cancelar una suscripcion
@router.post("/usuarios/{usuario_id}/cancelar/{fondo_id}", tags=["Negocio"])
async def cancelar_fondo(usuario_id: str, fondo_id: str):
    usuario = await db.usuarios.find_one({"_id": usuario_id})
    fondo = await db.fondos.find_one({"_id": fondo_id})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not fondo:
        raise HTTPException(status_code=404, detail="Fondo no encontrado")

    if usuario['saldo_fondos'][int(fondo_id)-1]==0:
        raise HTTPException(status_code=404, detail="No está suscrito a este fondo")

    # Reembolsar el monto y registrar la transacción
    usuario['saldo_disponible'] = usuario['saldo_disponible'] + usuario['saldo_fondos'][int(fondo_id)-1]
    retornado=usuario['saldo_fondos'][int(fondo_id)-1]
    usuario['saldo_fondos'][int(fondo_id)-1]=0
    usuario['transacciones'].append({
        "id": str(uuid.uuid4()),
        "id_fondo": fondo_id,
        "nombre_fondo": fondo['nombre'],
        "valor": retornado,
        "tipo_transaccion": "cancelacion",
        "fecha": datetime.now().isoformat()  # Agrega la fecha actual en formato ISO
    })
    await db.usuarios.replace_one({"_id": usuario_id}, usuario)

    return {"mensaje": "Cancelación exitosa", "saldo_actual": usuario['saldo_disponible']}

#Crear usuario
@router.post("/usuarios/", response_model=Usuario, tags=["Usuarios"])
async def crear_usuario(usuario: Usuario):
    resultado = await db.usuarios.insert_one(usuario.dict(by_alias=True))
    if resultado.inserted_id:
        usuario.id = str(resultado.inserted_id)
        return usuario
    raise HTTPException(status_code=500, detail="Error al crear el usuario")

#Ver todos los usuarios
@router.get("/usuarios/", response_model=List[Usuario], tags=["Usuarios"])
async def obtener_usuarios():
    usuarios = await db.usuarios.find().to_list(1000)
    return [Usuario(**usuario) for usuario in usuarios]

#Ver usuario por id
@router.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
async def obtener_usuario(usuario_id: str):
    usuario = await db.usuarios.find_one({"_id": usuario_id})
    if usuario:
        return Usuario(**usuario)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#Ver historial de transacciones
@router.get("/usuarios/{usuario_id}/historial", tags=["Usuarios"])
async def historial_transacciones(usuario_id: str):
    usuario = await db.usuarios.find_one({"_id": usuario_id})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario['transacciones']