# models/apci.py
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field
from datetime import time, date

Calif = Literal['B', 'R', 'M']          # Bien / Regular / Mal
TipoRec = Literal['A', 'C']             # A: Apertura, C: Cierre

class ApcDetIn(BaseModel):
    idEquipo: int = Field(..., gt=0)
    Calificacion: Calif
    Comentario: Optional[str] = Field(None, max_length=400)

class ApcIn(BaseModel):
    idCentro: str = Field(..., min_length=1, max_length=4)
    HoraI: time
    HoraF: Optional[time] = None
    Anfitrion: int = Field(..., ge=0)
    Plantilla: int = Field(..., ge=0)
    Candados: int = Field(..., ge=0)
    idUsuario: int = Field(..., gt=0)
    TipoRecorrido: TipoRec
    detalles: List[ApcDetIn] = Field(default_factory=list)

class ApcCreatedOut(BaseModel):
    estatus: int
    mensaje: str
    idApCi: int
    totalDetalles: int
