# SucursalesDAO.py
from typing import List, Dict, Any, Optional
from DAO.UsuariosDAO import get_conn  # ajusta al helper real

def list_sucursales() -> List[Dict[str, Any]]:
    """
    Lista general de sucursales (idCentro, Sucursales).
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT
            s.idCentro   AS idCentro,
            s.Sucursales AS Sucursales
        FROM sucursales s
        ORDER BY s.Sucursales
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def list_sucursales_no_asignadas(
    id_usuarios: int,
    q: Optional[str] = None,
    id_zona: Optional[int] = None,
    zona_nombre: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Devuelve sucursales que NO están asignadas al usuario indicado.
    Tablas/columnas reales:
      - met_usuariosuc(idUsuarios, idCentro)
      - sucursales(idCentro, Sucursales, idZona)
      - zonas(idZona, Zona)
    Filtros:
      - q:   busca por s.Sucursales o s.idCentro
      - id_zona: zonas.idZona
      - zona_nombre: zonas.Zona LIKE
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    params = {"id_usuarios": id_usuarios}
    where = [
        "NOT EXISTS (SELECT 1 FROM met_usuariosuc us WHERE us.idUsuarios = %(id_usuarios)s AND us.idCentro = s.idCentro)"
    ]

    if q:
        where.append("(s.Sucursales LIKE %(q)s OR s.idCentro LIKE %(q)s)")
        params["q"] = f"%{q}%"

    join_zona = ""
    if id_zona is not None:
        join_zona = "LEFT JOIN zonas z ON z.idZona = s.idZona"
        where.append("z.idZona = %(id_zona)s")
        params["id_zona"] = id_zona
    elif zona_nombre:
        join_zona = "LEFT JOIN zonas z ON z.idZona = s.idZona"
        where.append("z.Zona LIKE %(zona_nombre)s")
        params["zona_nombre"] = f"%{zona_nombre}%"

    where_sql = " AND ".join(where)

    sql = f"""
        SELECT
            s.idCentro   AS idCentro,
            s.Sucursales AS Sucursales
        FROM sucursales s
        {join_zona}
        WHERE {where_sql}
        ORDER BY s.Sucursales
    """
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
