# models/auth.py
from typing import Optional, Dict
from pydantic import BaseModel, Field

class AuthIn(BaseModel):
    idUsuarios: int = Field(..., gt=0)
    pwd: str = Field(..., min_length=1)

class UsuarioOut(BaseModel):
    user: int
    nombre: str
    idNivelUsuario: int
    estatus: int
    idCentro: Optional[str] = None  # si aplica

class AuthOut(BaseModel):
    estatus: int
    mensaje: str
    usuario: UsuarioOut
    idSesion: str
    token: str
    refreshToken: Optional[str] = None
    fechaLogin: str
    metadatos: Dict[str, Optional[str]]
