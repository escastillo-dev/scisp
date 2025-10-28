# security_basic.py
from typing import Optional, Dict, Any, Set
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from DAO.UsuariosDAO import  get_usuario_by_id, check_password

security = HTTPBasic()

# Niveles permitidos para administrar usuarios
ADMIN_LEVELS: Set[int] = {1, 2, 3, 4,6}  # ejemplo: 1=Admin, 2=Coordinador, 3=Supervisor

def require_roles(allowed_levels: Optional[Set[int]] = None):
    """Devuelve una dependencia que valida BasicAuth y nivel de usuario."""
    if allowed_levels is None:
        allowed_levels = ADMIN_LEVELS

    async def _dep(credentials: HTTPBasicCredentials = Depends(security)) -> Dict[str, Any]:
        # username debe ser el idUsuarios (int) según tu modelo
        try:
            user_id = int(credentials.username)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inválido")

        user = get_usuario_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

        if int(user["Estatus"]) != 1:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        if not check_password(credentials.password, user["Contraseña"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

        nivel = int(user["idNivelUsuario"])
        if nivel not in allowed_levels:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permisos insuficientes")

        # Devuelve el usuario autenticado para usarlo en el endpoint
        return {
            "IdUsuarios": user["IdUsuarios"],
            "NombreUsuario": user["NombreUsuario"],
            "idNivelUsuario": nivel,
            "Estatus": user["Estatus"],
        }

    return _dep
