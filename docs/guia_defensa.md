# Guía de defensa (qué decir y dónde mirar)

## Checkpoint de la Clase 7
| Piden | Dónde |
|---|---|
| Ejecutar `main.py`, registrar y listar | `python src/main.py` → opciones 1 y 2 |
| Dónde está el SQL | `persistencia/empleado_dao.py` (y el CREATE TABLE en `crear_bd.py`) |
| Dónde se configura la conexión | `persistencia/conexion.py` + `.env` |
| Responsabilidad de `dominio/` | Representa el problema (datos y reglas); no sabe de SQL |
| Responsabilidad de `persistencia/` | Conexión, SQL, CRUD y convertir filas en objetos |
| Responsabilidad de `main.py` | Menú, pedir datos, crear objetos, llamar al DAO, mostrar resultados |
| Una validación | `main.py` → `pedir_entero` (rechaza "abc") |
| Un try-except | `main.py` → `ejecutar()`; `empleado_dao.py` → `insertar()` |

## Paso 1 – Clases y constructores (2.1.1)
`Persona(nombre, correo)` y `Empleado(nombre, correo, cargo, id=None)`. `id=None` porque el objeto aún no está
guardado: la base de datos genera el id y el DAO lo asigna con `cursor.lastrowid`.

## Paso 2 – POO (2.1.2)
- **Encapsulamiento:** atributos con `_` y `@property`; los *setters* validan antes de cambiar el valor.
  (En Python el `_` es convención; la protección real son las validaciones.)
- **Herencia:** `Empleado` ES una `Persona`; `super().__init__()` reutiliza el constructor y evita repetir
  nombre/correo y sus reglas.
- **Polimorfismo:** `Empleado.mostrar_datos()` redefine el de `Persona` y lo extiende con `super()`.

## Paso 3 – Base de datos y CRUD (2.1.3)
- `DB_ENGINE` en `.env` elige motor. SQLite: módulo oficial `sqlite3`. MySQL: **PyMySQL**.
- Parámetros MySQL: host, port, user, password, database, charset `utf8mb4`. Las credenciales salen del `.env`
  (python-dotenv), no del código; `.env` no se publica.
- `marcador_sql()`: `?` en SQLite, `%s` en MySQL. Los datos van **siempre como parámetros**; en el f-string solo
  se interpola el marcador, nunca un dato del usuario (evita inyección SQL).
- `insertar` → INSERT + commit + `lastrowid` · `buscar_por_id`/`listar` → `fetchone`/`fetchall` y se devuelven
  objetos `Empleado` · `actualizar`/`eliminar` → `rowcount > 0` para saber si existía el registro.
- Buscar o eliminar un id inexistente es un **resultado normal** (`None` / `False`), no una excepción.

## Paso 4 – Errores y validaciones (2.1.4)
- **Validar** (antes, errores esperables): `pedir_entero` (solo dígitos), `pedir_texto` (no vacío), `pedir_correo` (formato).
- **Excepciones** (durante, inesperados): el DAO hace `rollback()` si falla, **re-lanza** el error y `finally` cierra la conexión.
  `main.ejecutar()` decide el mensaje: `ValueError` (regla del dominio), `ERRORES_INTEGRIDAD` (correo duplicado),
  `ERRORES_BD` (conexión/tabla), `Exception` (red final).
- Al iniciar, `main()` captura errores de configuración/conexión y termina con un mensaje claro.
- Demostrar un fallo: poner `DB_ENGINE=oracle` en `.env`, o registrar dos empleados con el mismo correo.

## Paso 5 – IA (2.1.5)
Completen `docs/registro_ia.md` con lo que realmente hicieron.
