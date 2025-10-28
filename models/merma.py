# models/merma.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class MotivoMerma(BaseModel):
    idMotMer: int
    Motivo: str

    class Config:
        from_attributes = True


class MermaBase(BaseModel):
    idCentro: str
    Fecha: date
    idUsuario: int
    Anfitrion: str  # Cambiado de int a str para número de nómina


class MermaCreate(BaseModel):
    idCentro: str
    Fecha: date
    idUsuario: int
    Anfitrion: str  # Número de nómina como string


class MermaUpdate(BaseModel):
    idCentro: Optional[str] = None
    Fecha: Optional[date] = None
    idUsuario: Optional[int] = None
    Anfitrion: Optional[str] = None  # Cambiado de int a str


class Merma(MermaBase):
    idMaMe: int
    nombreSucursal: Optional[str] = None
    nombreUsuario: Optional[str] = None

    class Config:
        from_attributes = True


class MermaResponse(BaseModel):
    estatus: int
    mensaje: str
    mermas: Optional[List[Merma]] = None
    merma: Optional[Merma] = None


class MotivoMermaResponse(BaseModel):
    estatus: int
    mensaje: str
    motivos: Optional[List[MotivoMerma]] = []


class MermaDetalleBase(BaseModel):
    idMaMe: int
    CodigoBarras: str
    idMotMer: int
    Cantidad: str


class MermaDetalleCreate(MermaDetalleBase):
    pass


class MermaDetalle(MermaDetalleBase):
    id_DetMaMe: int
    nombreProducto: Optional[str] = None
    descripcionMotivo: Optional[str] = None

    class Config:
        from_attributes = True