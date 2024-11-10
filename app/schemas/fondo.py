from pydantic import BaseModel, Field
from typing import List
from enum import Enum
import uuid

class categoriafondo(str,Enum):
    fpv= "FPV"
    fic= "FIC"

# Modelos de datos con Pydantic
class Fondo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    nombre: str
    monto_minimo: float
    categoria: categoriafondo

class Usuario(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    nombre: str
    correo: str
    telefono: int
    saldo_disponible: float
    saldo_fondos:list[float]=[0,0,0,0,0]
    transacciones: List[dict] = []