# models/niveles.py
from typing import List
from pydantic import BaseModel

class NivelItemOut(BaseModel):
    idNivelUsuario: int
    NivelUsuario: str

class NivelesOut(BaseModel):
    estatus: int
    mensaje: str
    niveles: List[NivelItemOut]
