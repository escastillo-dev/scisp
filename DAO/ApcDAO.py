from DAO.UsuariosDAO import get_conn
from typing import Optional, List, Dict, Any, Tuple
from pymysql.cursors import DictCursor


def sucursal_existe(id_centro: str) -> bool:
    conn = get_conn();
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM sucursales WHERE idCentro=%s", (id_centro,))
    ok = cur.fetchone() is not None
    cur.close();
    conn.close()
    return ok


def usuario_existe(id_usuario: int) -> bool:
    conn = get_conn();
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM usuarios WHERE IdUsuarios=%s AND Estatus=1", (id_usuario,))
    ok = cur.fetchone() is not None
    cur.close();
    conn.close()
    return ok


def equipos_existen(ids: List[int]) -> Tuple[bool, List[int]]:
    if not ids:
        return True, []
    conn = get_conn();
    cur = conn.cursor()
    cur.execute(
        f"SELECT idEquipo FROM met_equipos WHERE idEquipo IN ({','.join(['%s'] * len(ids))})",
        ids
    )
    presentes = {row[0] for row in cur.fetchall()}
    faltantes = [i for i in ids if i not in presentes]
    cur.close();
    conn.close()
    return len(faltantes) == 0, faltantes


def crear_apci(header: Dict[str, Any], detalles: List[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Inserta en met_apci y met_detapci dentro de una transacción.
    Devuelve (idApCi, totalDetalles).
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO met_apci
              (idCentro, HoraI, HoraF, Anfitrion, Plantilla, Candados, idUsuario, TipoRecorrido, Fecha)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s, CURDATE())
        """, (
            header["idCentro"],
            header["HoraI"],
            header.get("HoraF"),
            header["Anfitrion"],
            header["Plantilla"],
            header["Candados"],
            header["idUsuario"],
            header["TipoRecorrido"]
        ))
        id_apci = cur.lastrowid

        if detalles:
            cur.executemany("""
                INSERT INTO met_detapci
                  (idApCi, idEquipo, Calificacion, Comentario)
                VALUES (%s,%s,%s,%s)
            """, [
                (id_apci, d["idEquipo"], d["Calificacion"], d.get("Comentario"))
                for d in detalles
            ])

        conn.commit()
        total = len(detalles)
        cur.close()
        return id_apci, total
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _build_filters(
        sucursal: Optional[str],
        tipo: Optional[str],
        fecha_inicio: Optional[str],
        fecha_fin: Optional[str],
        usuario: Optional[int],
) -> Tuple[str, List]:
    """Construye los filtros SQL para la consulta."""
    conds: List[str] = []
    params: List = []

    if sucursal:
        conds.append("ma.idCentro = %s")
        params.append(sucursal)

    if tipo:
        conds.append("ma.TipoRecorrido = %s")
        params.append(tipo)

    if fecha_inicio:
        conds.append("ma.Fecha >= %s")  # CAMBIADO: era ma.date
        params.append(fecha_inicio)

    if fecha_fin:
        conds.append("ma.Fecha <= %s")  # CAMBIADO: era ma.date
        params.append(fecha_fin)

    if usuario:
        conds.append("ma.idUsuario = %s")
        params.append(usuario)

    if conds:
        where = "WHERE " + " AND ".join(conds)
    else:
        where = ""

    print(f"DEBUG _build_filters - WHERE: {where}, PARAMS: {params}")
    return where, params


def apci_count(
        sucursal: Optional[str],
        tipo: Optional[str],
        fecha_inicio: Optional[str],
        fecha_fin: Optional[str],
        usuario: Optional[int],
) -> int:
    """Obtiene el conteo total de registros."""
    conn = get_conn()
    cur = conn.cursor()
    where, params = _build_filters(sucursal, tipo, fecha_inicio, fecha_fin, usuario)

    sql = f"SELECT COUNT(*) FROM met_apci ma {where}"

    print(f"COUNT SQL: {sql}")
    print(f"COUNT PARAMS: {params}")

    cur.execute(sql, params)
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total


def apci_list(
        sucursal: Optional[str],
        tipo: Optional[str],
        fecha_inicio: Optional[str],
        fecha_fin: Optional[str],
        usuario: Optional[int],
        limit: int = 50,
        offset: int = 0
) -> List[Dict[str, Any]]:
    """Obtiene los registros de apertura/cierre con detalles."""
    print(f"DEBUG apci_list - Parámetros recibidos:")
    print(f"  sucursal: {sucursal}, tipo: {tipo}, fecha_inicio: {fecha_inicio}")
    print(f"  fecha_fin: {fecha_fin}, usuario: {usuario}, limit: {limit}, offset: {offset}")

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    where, params = _build_filters(sucursal, tipo, fecha_inicio, fecha_fin, usuario)

    # Query principal para obtener registros básicos
    sql = f"""
    SELECT  
        ma.idApCi,
        ma.idCentro,
        ma.Fecha AS fecha,
        ma.HoraI AS horaInicio,
        ma.HoraF AS horaFin,
        ma.TipoRecorrido AS tipoRecorrido,
        ma.Anfitrion AS anfitrion,
        ma.Plantilla AS plantilla,
        ma.Candados AS candados,
        ma.idUsuario AS usuario
    FROM met_apci ma
    {where}
    ORDER BY ma.Fecha DESC, ma.HoraI DESC
    LIMIT %s OFFSET %s
    """

    final_params = params + [limit, offset]

    print(f"DEBUG SQL: {sql}")
    print(f"DEBUG PARAMS: {final_params}")

    try:
        cur.execute(sql, final_params)
        rows = cur.fetchall()

        print(f"DEBUG - Registros encontrados: {len(rows)}")

        # Procesar cada registro
        for r in rows:
            # Campos básicos
            r["sucursalNombre"] = f"Sucursal {r['idCentro']}"
            r["anfitrionNombre"] = f"Usuario {r['anfitrion']}"
            r["usuarioNombre"] = f"Usuario {r['usuario']}"

            # Convertir fecha y hora
            if hasattr(r['fecha'], 'strftime'):
                r['fecha'] = r['fecha'].strftime('%Y-%m-%d')
            elif isinstance(r['fecha'], str):
                r['fecha'] = r['fecha']

            for campo_hora in ['horaInicio', 'horaFin']:
                if r[campo_hora] and hasattr(r[campo_hora], 'total_seconds'):
                    total_seconds = int(r[campo_hora].total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    r[campo_hora] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                elif isinstance(r[campo_hora], str):
                    r[campo_hora] = r[campo_hora]

            # CALCULAR CALIFICACIÓN Y ESTADO REAL basándose en los detalles
            detalles_sql = """
            SELECT 
                md.idEquipo,
                COALESCE(e.Equipo, 'Equipo desconocido') AS equipoNombre,
                md.Calificacion AS calificacion,
                md.Comentario AS comentario
            FROM met_detapci md
            LEFT JOIN met_equipos e ON e.idEquipo = md.idEquipo
            WHERE md.idApCi = %s
            ORDER BY md.idEquipo
            """

            cur.execute(detalles_sql, (r["idApCi"],))
            detalles = cur.fetchall()
            r["detalles"] = detalles

            # CALCULAR CALIFICACIÓN PROMEDIO REAL
            if detalles:
                valores_calificacion = []
                equipos_problema = 0

                for detalle in detalles:
                    cal = detalle['calificacion']
                    if cal == 'B':  # Bien
                        valores_calificacion.append(10)
                    elif cal == 'R':  # Regular
                        valores_calificacion.append(6)
                    elif cal == 'M':  # Mal
                        valores_calificacion.append(2)
                        equipos_problema += 1

                # Calcular promedio
                if valores_calificacion:
                    promedio = sum(valores_calificacion) / len(valores_calificacion)
                    r["calificacionPromedio"] = round(promedio, 1)
                else:
                    r["calificacionPromedio"] = 0.0

                r["totalEquipos"] = len(detalles)
                r["equiposProblema"] = equipos_problema

                # DETERMINAR ESTADO REAL
                if equipos_problema > 0:
                    r["estado"] = "con_problemas"
                else:
                    r["estado"] = "completado"
            else:
                # Sin detalles
                r["calificacionPromedio"] = 0.0
                r["totalEquipos"] = 0
                r["equiposProblema"] = 0
                r["estado"] = "sin_evaluar"

        print(f"DEBUG - Registros después de procesamiento: {rows}")

        cur.close()
        conn.close()
        return rows

    except Exception as e:
        print(f"ERROR EN apci_list: {str(e)}")
        import traceback
        traceback.print_exc()
        cur.close()
        conn.close()
        return []

def apci_list_simple(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Versión simple para debugging"""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    sql = """
    SELECT  
        ma.idApCi,
        ma.idCentro,
        ma.date AS fecha,
        ma.HoraI AS horaInicio,
        ma.HoraF AS horaFin,
        ma.TipoRecorrido AS tipoRecorrido
    FROM met_apci ma
    ORDER BY ma.idApCi DESC
    LIMIT %s OFFSET %s
    """

    try:
        cur.execute(sql, [limit, offset])
        rows = cur.fetchall()

        # Agregar campos por defecto
        for r in rows:
            r["sucursalNombre"] = "Test"
            r["anfitrion"] = 0
            r["anfitrionNombre"] = "Test"
            r["plantilla"] = 0
            r["candados"] = 0
            r["usuario"] = 0
            r["usuarioNombre"] = "Test"
            r["calificacionPromedio"] = 10.0
            r["totalEquipos"] = 0
            r["equiposProblema"] = 0
            r["estado"] = "completado"
            r["detalles"] = []

        cur.close()
        conn.close()
        return rows

    except Exception as e:
        print(f"ERROR: {str(e)}")
        cur.close()
        conn.close()
        return []