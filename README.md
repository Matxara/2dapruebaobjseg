# EcoTech – CRUD de empleados (Python + SQLite/MySQL)

Integrantes: _(completar)_ · Líder de proyecto: _(completar)_

## Ejecutar en un entorno limpio
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1        # Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env            # por defecto usa SQLite
python src/main.py
```
Si PowerShell bloquea la activación: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`.

Para usar MySQL: en `.env` poner `DB_ENGINE=mysql` y completar host, puerto, base, usuario y clave
(ver `.env.example`). No se cambia ninguna línea de código.

## Estructura
```
src/
├── main.py                 menú, validación de entradas y coordinación (sin SQL)
├── dominio/
│   ├── persona.py          clase base: nombre y correo + validaciones
│   └── empleado.py         Empleado hereda de Persona; agrega cargo e id
└── persistencia/
    ├── conexion.py         lee .env y abre SQLite o MySQL
    ├── crear_bd.py         crea la tabla
    └── empleado_dao.py     todo el SQL (insertar, buscar, listar, actualizar, eliminar)
```
Flujo: `Usuario → main.py → Empleado → EmpleadoDAO → conexion.py → SQLite/MySQL`
