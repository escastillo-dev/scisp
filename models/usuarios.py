# models/usuarios.py
from __future__ import annotations

from typing import Optional, Dict, List
from pydantic import BaseModel, Field, validator,root_validator
from datetime import date

class UsuarioCreateIn(BaseModel):
    idUsuarios: int = Field(..., gt=0)
    NombreUsuario: str = Field(..., min_length=3, max_length=45)
    pwd: str = Field(..., min_length=8)  # min. 8 y combina (valida abajo)
    idNivelUsuario: int = Field(..., alias="idNivelUsuario")
    estatus: int = Field(default=1)  # A/I o 1/0
    idCentro: str = Field(..., min_length=1, max_length=10)

    @validator("pwd")
    def strong_pwd(cls, v: str):
        # Reglas simples: 8+, al menos una letra y un dígito (ajusta si quieres symbols)
        if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe incluir letras y números")
        return v

class UsuarioCreatedOut(BaseModel):
    estatus: int
    mensaje: str
    usuario: Dict[str, object]

class UsuarioUpdateIn(BaseModel):
    # Campos opcionales (solo se actualiza lo que venga)
    NombreUsuario: Optional[str] = Field(None, min_length=3, max_length=45)
    idNivelUsuario: Optional[int] = Field(None, gt=0)
    estatus: Optional[int] = Field(None, ge=0, le=1)   # 0/1
    idCentro: Optional[str] = Field(None, min_length=1, max_length=10)  # reasignación/alta en UsuarioSuc

    # @root_validator
    # def at_least_one(cls, values):
    #     if not any(v is not None for v in values.values()):
    #         raise ValueError("Debe enviar al menos un campo a modificar")
    #     return values

class UsuarioUpdatedOut(BaseModel):
    estatus: int
    mensaje: str
    usuario: Dict[str, object]

class UsuarioBasic(BaseModel):
    idUsuarios: int
    NombreUsuario: str
    idNivelUsuario: int
    estatus: int
    FechaAlta: Optional[str] = None

class NivelInfo(BaseModel):
    idNivelUsuario: int
    NivelUsuario: str

class SucursalInfo(BaseModel):
    idCentro: str
    Sucursal: str

class UsuarioGetOut(BaseModel):
    estatus: int
    mensaje: str
    usuario: UsuarioBasic
    nivel: Optional[NivelInfo] = None          # 👈 antes: NivelInfo | None
    sucursales: List[SucursalInfo] = []

class AsignarSucursalIn(BaseModel):
    idCentro: str = Field(..., min_length=1, max_length=10)

class AsignarSucursalOut(BaseModel):
    estatus: int
    mensaje: str
    asignacion: Dict[str, object]

class UsuarioBajaOut(BaseModel):
    estatus: int
    mensaje: str
    usuario: Dict[str, int]

class UsuariosQueryIn(BaseModel):
    """Query params para listar usuarios."""
    limit: int = Field(50, ge=1, le=200)
    offset: int = Field(0, ge=0)
    estatus: Optional[int] = Field(None, description="1=activo, 0=baja")
    idNivelUsuario: Optional[int] = None
    q: Optional[str] = Field(None, description="Búsqueda por id o nombre")

class UsuarioListItemOut(BaseModel):
    idUsuarios: int
    NombreUsuario: str
    idNivelUsuario: int
    estatus: int
    FechaAlta: Optional[date] = None
    nivel: Optional[str] = None
    sucursales: int = 0  # cantidad de sucursales asignadas

class UsuariosPageOut(BaseModel):
    estatus: int
    mensaje: str
    total: int
    limit: int
    offset: int
    usuarios: List[UsuarioListItemOut]