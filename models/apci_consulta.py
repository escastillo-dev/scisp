from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DetalleOut(BaseModel):
    idEquipo: int
    equipoNombre: str
    calificacion: Optional[str] = None
    comentario: Optional[str] = None

class ApcRegistroOut(BaseModel):
    idApCi: int
    idCentro: str
    sucursalNombre: Optional[str] = None
    fecha: str  # Cambié a str para evitar problemas de conversión
    horaInicio: Optional[str] = None
    horaFin: Optional[str] = None
    anfitrion: Optional[int] = None
    anfitrionNombre: Optional[str] = None
    plantilla: Optional[int] = None
    candados: Optional[int] = None
    tipoRecorrido: str
    usuario: Optional[int] = None
    usuarioNombre: Optional[str] = None
    calificacionPromedio: Optional[float] = None
    totalEquipos: int
    equiposProblema: int
    estado: str
    detalles: List[DetalleOut]

# AGREGADO: Modelo de respuesta que faltaba
class ApcConsultaResp(BaseModel):
    estatus: int
    mensaje: str
    registros: List[ApcRegistroOut]
    total: Optional[int] = None
    pagina: Optional[int] = None