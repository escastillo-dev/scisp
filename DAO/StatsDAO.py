# StatsDAO.py
from typing import Dict, Any
from DAO.UsuariosDAO import get_conn  # tu helper de conexión

def get_dashboard_stats(activos: bool = True) -> Dict[str, Any]:
    """
    Obtiene:
      - totalUsuarios (activos si activos=True, de lo contrario todos)
      - usuariosPorZona: { idZona: { nombre, total } }
      - usuariosPorNivel: { idNivelUsuario: { nombre, total } }
    Todo en UNA sola consulta SQL usando UNION ALL.
    """

    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    where_estatus = "u.Estatus = 1" if activos else "1=1"

    sql = f"""
    -- Total de usuarios
    (SELECT
        'TOTAL' AS kind,
        NULL     AS id_key,
        COUNT(*) AS total,
        NULL     AS nombre
     FROM usuarios u
     WHERE {where_estatus}
    )
    UNION ALL
    -- Usuarios por ZONA (contando usuarios distintos por zona)
    (SELECT
        'ZONA'           AS kind,
        CAST(z.idZona AS CHAR) AS id_key,
        COUNT(DISTINCT u.IdUsuarios) AS total,
        z.Zona           AS nombre
     FROM usuarios u
     JOIN met_usuariosuc us ON us.idUsuarios = u.IdUsuarios
     JOIN sucursales s      ON s.idCentro    = us.idCentro
     JOIN zonas z           ON z.idZona      = s.idZona
     WHERE {where_estatus}
     GROUP BY z.idZona, z.Zona
    )
    UNION ALL
    -- Usuarios por NIVEL
    (SELECT
        'NIVEL'                    AS kind,
        CAST(u.idNivelUsuario AS CHAR) AS id_key,
        COUNT(*)                  AS total,
        n.NivelUsuario            AS nombre
     FROM usuarios u
     LEFT JOIN nivelusuarios n ON n.idNivelUsuario = u.idNivelUsuario
     WHERE {where_estatus}
     GROUP BY u.idNivelUsuario, n.NivelUsuario
    );
    """

    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Armar estructura final
    total_usuarios = 0
    usuarios_por_zona: Dict[str, Any] = {}
    usuarios_por_nivel: Dict[str, Any] = {}

    for r in rows:
        kind   = r["kind"]
        id_key = r["id_key"]
        total  = int(r["total"])
        nombre = r["nombre"]

        if kind == "TOTAL":
            total_usuarios = total

        elif kind == "ZONA" and id_key is not None:
            usuarios_por_zona[id_key] = {
                "nombre": nombre or "",
                "total": total
            }

        elif kind == "NIVEL" and id_key is not None:
            usuarios_por_nivel[id_key] = {
                "nombre": nombre or "",
                "total": total
            }

    return {
        "totalUsuarios": total_usuarios,
        "usuariosPorZona": usuarios_por_zona,
        "usuariosPorNivel": usuarios_por_nivel
    }
