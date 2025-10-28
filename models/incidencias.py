# models/incidencias.py
from typing import List, Optional
from pydantic import BaseModel, Field

class IncidenciaItemOut(BaseModel):
    idIncidencia: int
    Incidencia: str

class IncidenciaIn(BaseModel):
    Incidencia: str = Field(..., min_length=2, max_length=100)

class IncidenciaGetOut(BaseModel):
    estatus: int
    mensaje: str
    incidencia: Optional[IncidenciaItemOut] = None

class IncidenciasOut(BaseModel):
    estatus: int
    mensaje: str
    total: int
    incidencias: List[IncidenciaItemOut]
