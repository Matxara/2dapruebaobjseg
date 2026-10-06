"""EmpleadoDAO: aquí vive TODO el SQL de la aplicación.

Patrón de cada método: abrir conexión -> ejecutar con parámetros ->
commit (o rollback si falla) -> cerrar siempre. Los errores se propagan
hacia main.py, que decide qué mensaje mostrar al usuario.
"""
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql

_COLUMNAS = "id, nombre, correo, cargo"


class EmpleadoDAO:
    @staticmethod
    def _fila_a_empleado(fila):
        """Transforma una fila de la BD en un objeto Empleado."""
        return Empleado(id=fila[0], nombre=fila[1], correo=fila[2], cargo=fila[3])

    @staticmethod
    def insertar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            cursor.execute(
                f"INSERT INTO empleado (nombre, correo, cargo) VALUES ({m}, {m}, {m})",
                (empleado.nombre, empleado.correo, empleado.cargo),
            )
            conexion.commit()
            empleado.id = cursor.lastrowid  # el id lo genera la BD
            return empleado
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM empleado WHERE id = {marcador_sql()}", (id_empleado,)
            )
            fila = cursor.fetchone()
            return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_correo(correo):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM empleado WHERE correo = {marcador_sql()}",
                (correo.strip().lower(),),
            )
            fila = cursor.fetchone()
            return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar():
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM empleado ORDER BY id")
            return [EmpleadoDAO._fila_a_empleado(f) for f in cursor.fetchall()]
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def actualizar(empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            m = marcador_sql()
            cursor.execute(
                f"UPDATE empleado SET nombre = {m}, correo = {m}, cargo = {m} WHERE id = {m}",
                (empleado.nombre, empleado.correo, empleado.cargo, empleado.id),
            )
            conexion.commit()
            return cursor.rowcount > 0  # False si no existía ese id
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute(f"DELETE FROM empleado WHERE id = {marcador_sql()}", (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0  # False si no existía ese id
        except Exception:
            if conexion:
                conexion.rollback()
            raise
        finally:
            if conexion:
                conexion.close()
