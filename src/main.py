"""Punto de entrada: muestra el menú, pide datos y coordina objetos y DAO.

main.py NO contiene SQL ni credenciales.
"""
from dominio.empleado import Empleado
from dominio.persona import validar_correo
from persistencia.conexion import ERRORES_BD, ERRORES_INTEGRIDAD
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO


# ------------------------------------------------- validación de entradas
def pedir_texto(mensaje, obligatorio=True):
    """Valida ANTES de usar el dato: no acepta vacío si es obligatorio."""
    while True:
        texto = input(mensaje).strip()
        if texto or not obligatorio:
            return texto
        print("Este dato es obligatorio.")


def pedir_entero(mensaje):
    """Valida que el texto sean solo dígitos antes de convertirlo."""
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("Debe ingresar un número entero positivo.")


def pedir_correo(mensaje, opcional=False):
    """Pide un correo y lo valida con la misma regla que usa el dominio."""
    while True:
        texto = input(mensaje).strip()
        if opcional and texto == "":
            return ""
        try:
            return validar_correo(texto)
        except ValueError as error:  # excepción: la regla del dominio rechazó el dato
            print(error)


# --------------------------------------------------------- operaciones CRUD
def registrar_empleado():
    nombre = pedir_texto("Nombre: ")
    correo = pedir_correo("Correo: ")
    cargo = pedir_texto("Cargo: ")
    empleado = Empleado(nombre, correo, cargo)  # nace con id=None
    EmpleadoDAO.insertar(empleado)              # la BD genera el id
    print(f"Empleado registrado con ID {empleado.id}.")


def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("No hay empleados registrados.")
    for empleado in empleados:
        print(" ", empleado.mostrar_datos())


def buscar_empleado():
    empleado = EmpleadoDAO.buscar_por_id(pedir_entero("ID del empleado: "))
    print(" ", empleado.mostrar_datos() if empleado else "No existe un empleado con ese ID.")


def actualizar_empleado():
    empleado = EmpleadoDAO.buscar_por_id(pedir_entero("ID del empleado: "))
    if empleado is None:
        print("No existe un empleado con ese ID.")
        return
    print("Datos actuales:", empleado.mostrar_datos(), "\n(Enter conserva el valor actual)")
    nombre = pedir_texto(f"Nombre [{empleado.nombre}]: ", obligatorio=False)
    correo = pedir_correo(f"Correo [{empleado.correo}]: ", opcional=True)
    cargo = pedir_texto(f"Cargo [{empleado.cargo}]: ", obligatorio=False)
    if nombre:
        empleado.nombre = nombre
    if correo:
        empleado.correo = correo
    if cargo:
        empleado.cargo = cargo
    if EmpleadoDAO.actualizar(empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("Empleado no encontrado.")


def eliminar_empleado():
    if EmpleadoDAO.eliminar(pedir_entero("ID del empleado a eliminar: ")):
        print("Empleado eliminado.")
    else:
        print("No existe un empleado con ese ID.")


# ------------------------------------------------------------ menú y errores
ACCIONES = {
    "1": registrar_empleado,
    "2": listar_empleados,
    "3": buscar_empleado,
    "4": actualizar_empleado,
    "5": eliminar_empleado,
}


def mostrar_menu():
    print("\n===== ECOTECH =====")
    print("1. Registrar empleado")
    print("2. Listar empleados")
    print("3. Buscar empleado por ID")
    print("4. Actualizar empleado")
    print("5. Eliminar empleado")
    print("0. Salir")


def ejecutar(accion):
    """Ejecuta una opción y convierte cualquier fallo en un mensaje seguro.

    El DAO detecta y propaga el error; aquí se decide qué comunicar,
    sin mostrar tracebacks ni detalles internos.
    """
    try:
        accion()
    except ValueError as error:          # regla del dominio
        print(f"Dato no válido: {error}")
    except ERRORES_INTEGRIDAD:           # correo duplicado
        print("No se pudo guardar: ya existe un empleado con ese correo.")
    except ERRORES_BD:                   # conexión caída, tabla inexistente, etc.
        print("No fue posible completar la operación en la base de datos.")
    except Exception:                    # red de seguridad final
        print("Ocurrió un error inesperado.")


def main():
    try:
        crear_tablas()
    except (ValueError, *ERRORES_BD):    # configuración errónea o servidor inaccesible
        print("No fue posible conectar con la base de datos. Revise su archivo .env.")
        return

    try:
        while True:
            mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                print("Hasta luego.")
                break
            if opcion in ACCIONES:
                ejecutar(ACCIONES[opcion])
            else:
                print("Opción no válida.")
    except (KeyboardInterrupt, EOFError):
        print("\nAplicación finalizada.")


if __name__ == "__main__":
    main()
