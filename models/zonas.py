# models/zonas.py
from typing import List
from pydantic import BaseModel

class ZonaItemOut(BaseModel):
    idZona: int
    Zona: str

class ZonasOut(BaseModel):
    estatus: int
    mensaje: str
    zonas: List[ZonaItemOut]
