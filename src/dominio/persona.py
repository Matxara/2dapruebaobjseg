"""Clase base Persona: datos y reglas comunes (nombre y correo)."""
import re

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_texto(valor, campo, maximo=100):
    """Texto obligatorio, sin espacios sobrantes y con largo máximo."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El {campo} no puede estar vacío.")
    limpio = valor.strip()
    if len(limpio) > maximo:
        raise ValueError(f"El {campo} no puede superar los {maximo} caracteres.")
    return limpio


def validar_correo(valor):
    """Correo con formato usuario@dominio.ext, en minúsculas."""
    texto = validar_texto(valor, "correo", 150)
    if not _PATRON_CORREO.match(texto):
        raise ValueError("El correo no tiene un formato válido (ej: ana@ecotech.cl).")
    return texto.lower()


class Persona:
    """Encapsula nombre y correo: solo se modifican a través de reglas de validación."""

    def __init__(self, nombre, correo):
        self._nombre = validar_texto(nombre, "nombre")
        self._correo = validar_correo(correo)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = validar_correo(valor)

    def mostrar_datos(self):
        return f"{self._nombre} - {self._correo}"

    def __str__(self):
        return self.mostrar_datos()
