# NivelesDAO.py
from typing import List, Dict, Any
from DAO.UsuariosDAO import get_conn

def list_niveles() -> List[Dict[str, Any]]:
    """
      Devuelve todos los niveles de usuario.
      Tabla esperada: nivelusuarios(IdNivelUsuario, NivelUsuario)
      """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
          SELECT
              IdNivelUsuario AS idNivelUsuario,
              NivelUsuario   AS NivelUsuario
          FROM nivelusuarios
          ORDER BY NivelUsuario
      """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows