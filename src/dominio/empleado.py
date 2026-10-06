"""Clase Empleado (dominio). No conoce SQL ni la base de datos."""
from dominio.persona import Persona, validar_texto


class Empleado(Persona):
    """Un Empleado ES una Persona (herencia) y además tiene cargo e identidad persistente."""

    def __init__(self, nombre, correo, cargo, id=None):
        super().__init__(nombre, correo)  # reutiliza el constructor y las validaciones de Persona
        self._cargo = validar_texto(cargo, "cargo")
        self.id = id  # None hasta que la BD genere el identificador

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if valor is not None and (isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0):
            raise ValueError("El id debe ser un entero positivo o None.")
        self._id = valor

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, valor):
        self._cargo = validar_texto(valor, "cargo")

    def mostrar_datos(self):
        """Polimorfismo: redefine el método de Persona agregando id y cargo."""
        return f"[{self._id}] {super().mostrar_datos()} - {self._cargo}"
