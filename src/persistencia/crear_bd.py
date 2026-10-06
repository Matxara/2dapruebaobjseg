"""Crea la tabla empleado según el motor activo."""
from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    if obtener_motor() == "sqlite":
        sql = """
            CREATE TABLE IF NOT EXISTS empleado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                cargo TEXT NOT NULL
            )"""
    else:
        sql = """
            CREATE TABLE IF NOT EXISTS empleado (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) NOT NULL UNIQUE,
                cargo VARCHAR(100) NOT NULL
            )"""
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()
