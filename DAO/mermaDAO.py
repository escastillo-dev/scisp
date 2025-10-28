# DAO/mermaDAO.py
from typing import List, Optional, Dict, Any
import mysql.connector
from mysql.connector import Error
from models.merma import Merma, MermaCreate, MermaUpdate, MermaDetalle, MermaDetalleCreate, MotivoMerma
from datetime import date
from DAO.UsuariosDAO import get_conn


def get_motivos_merma() -> List[MotivoMerma]:
    """Obtener todos los motivos de merma disponibles"""
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT idMotMer, Motivo FROM met_motmerma ORDER BY Motivo"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        motivos = []
        for row in results:
            motivo = MotivoMerma(
                idMotMer=row['idMotMer'],
                Motivo=row['Motivo']
            )
            motivos.append(motivo)
        return motivos
    except Error as e:
        print(f"Error fetching motivos merma: {e}")
        return []


def get_productos_catalogo(filtro: str = None) -> List[dict]:
    """Obtener productos del catálogo para búsqueda"""
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        if filtro:
            query = """
                SELECT CodigoBarras, Producto, idCategoria, idSubcategoria, Precio
                FROM catalogo 
                WHERE Producto LIKE %s OR CodigoBarras LIKE %s
                ORDER BY Producto
                LIMIT 50
            """
            cursor.execute(query, (f"%{filtro}%", f"%{filtro}%"))
        else:
            query = """
                SELECT CodigoBarras, Producto, idCategoria, idSubcategoria, Precio
                FROM catalogo 
                ORDER BY Producto
                LIMIT 100
            """
            cursor.execute(query)

        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as e:
        print(f"Error fetching productos: {e}")
        return []


def crear_merma_cabecera(merma_data: MermaCreate, id_usuario: int) -> Optional[int]:
    """Crear registro en met_mame y retornar el ID generado"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        query = """
            INSERT INTO met_mame (idCentro, Fecha, idUsuario, Anfitrion)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (
            merma_data.idCentro,
            merma_data.Fecha,
            id_usuario,  # Usar el ID del usuario autenticado
            merma_data.Anfitrion  # Ya es string, no necesita conversión
        ))

        merma_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Merma creada con ID: {merma_id}")
        return merma_id

    except Error as e:
        print(f"Error al crear merma cabecera: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None


def agregar_producto_detalle(merma_id: int, producto_data: dict) -> bool:
    """Agregar un producto al detalle de la merma (met_detmame)"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        print(f"Insertando producto en met_detmame:")
        print(f"  idMaMe: {merma_id}")
        print(f"  CodigoBarras: {producto_data['CodigoBarras']}")
        print(f"  idMotMer: {producto_data['idMotMer']}")
        print(f"  Cantidad: {producto_data['Cantidad']}")

        query = """
            INSERT INTO met_detmame (idMaMe, CodigoBarras, idMotMer, Cantidad)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (
            merma_id,
            producto_data['CodigoBarras'],
            producto_data['idMotMer'],
            producto_data['Cantidad']
        ))

        affected_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Filas afectadas: {affected_rows}")
        print(f"Producto agregado al detalle de merma {merma_id}")
        return True

    except Error as e:
        print(f"Error al agregar producto al detalle: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def get_mermas_by_sucursales(sucursales_ids: List[str]) -> List[Dict[str, Any]]:
    """Obtener mermas filtradas por sucursales"""
    try:
        print(f"=== INICIO get_mermas_by_sucursales ===")
        print(f"sucursales_ids recibido: {sucursales_ids}")
        print(f"Tipo: {type(sucursales_ids)}")

        conn = get_conn()
        print(f"Conexión obtenida: {conn}")

        cursor = conn.cursor(dictionary=True)
        print("Cursor creado")

        # Crear placeholders para la consulta IN
        placeholders = ','.join(['%s'] * len(sucursales_ids))
        print(f"Placeholders: {placeholders}")

        query = f"""
            SELECT 
                m.idMaMe,
                m.idCentro,
                m.Fecha,
                m.idUsuario,
                m.Anfitrion,
                COALESCE(s.Sucursales, 'Sin nombre') as nombreSucursal,
                COALESCE(u.NombreUsuario, 'Usuario no encontrado') as nombreUsuario
            FROM met_mame m
            LEFT JOIN sucursales s ON m.idCentro = s.idCentro
            LEFT JOIN usuarios u ON m.idUsuario = u.IdUsuarios
            WHERE m.idCentro IN ({placeholders})
            ORDER BY m.Fecha DESC, m.idMaMe DESC
        """

        print(f"Query generado: {query}")
        print(f"Parámetros: {sucursales_ids}")

        cursor.execute(query, sucursales_ids)
        results = cursor.fetchall()

        print(f"=== RESULTADOS ===")
        print(f"Número de filas: {len(results)}")
        print(f"Primeros 2 resultados: {results[:2] if results else 'Ninguno'}")

        cursor.close()
        conn.close()

        print(f"=== FIN get_mermas_by_sucursales - Retornando {len(results)} registros ===")
        return results

    except Error as e:
        print(f"=== ERROR en get_mermas_by_sucursales ===")
        print(f"Error MySQL: {e}")
        import traceback
        traceback.print_exc()
        return []
    except Exception as e:
        print(f"=== ERROR GENERAL en get_mermas_by_sucursales ===")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_productos_merma(merma_id: int) -> List[Dict[str, Any]]:
    """Obtener productos del detalle de una merma"""
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                d.id_DetMaMe,
                d.idMaMe,
                d.CodigoBarras,
                d.idMotMer,
                d.Cantidad,
                c.Precio,
                c.Producto as nombreProducto,
                mot.Motivo as descripcionMotivo
            FROM met_detmame d
            LEFT JOIN catalogo c ON d.CodigoBarras = c.CodigoBarras
            LEFT JOIN met_motmerma mot ON d.idMotMer = mot.idMotMer
            WHERE d.idMaMe = %s
            ORDER BY d.id_DetMaMe
        """

        cursor.execute(query, (merma_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return results

    except Error as e:
        print(f"Error al obtener productos de merma: {e}")
        return []


def eliminar_producto_detalle(merma_id: int, detalle_id: int) -> bool:
    """Eliminar un producto del detalle de merma"""
    try:
        conn = get_conn()
        cursor = conn.cursor()

        query = "DELETE FROM met_detmame WHERE idMaMe = %s AND id_DetMaMe = %s"
        cursor.execute(query, (merma_id, detalle_id))

        affected_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()

        return affected_rows > 0

    except Error as e:
        print(f"Error al eliminar producto del detalle: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def get_merma_by_id(merma_id: int) -> Optional[Dict[str, Any]]:
    """Obtener una merma por su ID - versión simplificada"""
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM met_mame WHERE idMaMe = %s"
        cursor.execute(query, (merma_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            print(f"Merma encontrada: {result}")
            # Agregar campos opcionales
            result["nombreSucursal"] = "Sucursal"
            result["nombreUsuario"] = "Usuario"
            return result
        else:
            print(f"No se encontró merma con ID: {merma_id}")
            return None

    except Error as e:
        print(f"Error al obtener merma por ID: {e}")
        return None