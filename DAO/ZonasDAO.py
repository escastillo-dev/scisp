# ZonasDAO.py
from typing import List, Dict, Any, Optional
from DAO.UsuariosDAO import get_conn  # ajusta al helper que ya usas

def list_zonas(q: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Devuelve idZona y Zona. Permite filtro opcional por nombre.
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    if q:
        cur.execute(
            """
            SELECT z.idZona AS idZona, z.Zona AS Zona
            FROM zonas z
            WHERE z.Zona LIKE %s
            ORDER BY z.Zona
            """,
            (f"%{q}%",)
        )
    else:
        cur.execute(
            """
            SELECT z.idZona AS idZona, z.Zona AS Zona
            FROM zonas z
            ORDER BY z.Zona
            """
        )

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
