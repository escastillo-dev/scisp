# IncidenciasDAO.py
from typing import List, Dict, Any, Optional, Tuple
from DAO.UsuariosDAO import get_conn  # usa tu helper real

def list_incidencias(q: Optional[str], limit: int, offset: int) -> Tuple[List[Dict[str, Any]], int]:
    """
    Lista incidencias con filtro opcional y paginación.
    Devuelve (rows, total).
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    where = []
    params = {}
    if q:
        where.append("i.Incidencia LIKE %(q)s")
        params["q"] = f"%{q}%"

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    cur.execute(f"SELECT COUNT(*) AS total FROM met_incmanval i {where_sql}", params)
    total = int(cur.fetchone()["total"])

    cur.execute(
        f"""
        SELECT i.idIncidencia, i.Incidencia
        FROM met_incmanval i
        {where_sql}
        ORDER BY i.Incidencia
        LIMIT %(limit)s OFFSET %(offset)s
        """,
        {**params, "limit": limit, "offset": offset}
    )
    rows = cur.fetchall()

    cur.close(); conn.close()
    return rows, total


def get_incidencia(id_inc: int) -> Optional[Dict[str, Any]]:
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT idIncidencia, Incidencia FROM met_incmanval WHERE idIncidencia=%s", (id_inc,))
    row = cur.fetchone()
    cur.close(); conn.close()
    return row


def create_incidencia(nombre: str) -> int:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO met_incmanval (Incidencia) VALUES (%s)", (nombre,))
    conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return new_id


def update_incidencia(id_inc: int, nombre: str) -> int:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE met_incmanval SET Incidencia=%s WHERE idIncidencia=%s", (nombre, id_inc))
    conn.commit()
    cnt = cur.rowcount
    cur.close(); conn.close()
    return cnt


def safe_delete_incidencia(id_inc: int) -> Tuple[bool, str]:
    """
    Borra si la incidencia NO está referenciada en met_detmanval.idIncidencia.
    """
    conn = get_conn(); cur = conn.cursor(dictionary=True)

    # ¿tiene referencias?
    cur.execute("SELECT 1 FROM met_detmanval WHERE idIncidencia=%s LIMIT 1", (id_inc,))
    if cur.fetchone():
        cur.close(); conn.close()
        return False, "No se puede eliminar: incidencia en uso (met_detmanval)."

    cur = conn.cursor()
    cur.execute("DELETE FROM met_incmanval WHERE idIncidencia=%s", (id_inc,))
    conn.commit()
    ok = cur.rowcount > 0
    cur.close(); conn.close()
    return ok, "Eliminado" if ok else "No existe el idIncidencia."
