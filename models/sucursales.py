# models/sucursales.py
from typing import List
from pydantic import BaseModel

class SucursalItemOut(BaseModel):
    idCentro: str
    Sucursales: str

class SucursalesOut(BaseModel):
    estatus: int
    mensaje: str
    sucursales: List[SucursalItemOut]
