# Registro de uso de IA (criterio 2.1.5)

> Debe reflejar lo que ustedes realmente hicieron. Verifiquen cada hallazgo ejecutando el código y completen
> las columnas marcadas. Borren lo que no hayan comprobado.

## Herramientas y fragmentos
| Herramienta | Fragmentos apoyados (archivo/función) | Nivel (borrador/completo) | Quién lo explica |
|---|---|---|---|
| Claude | _(completar)_ | _(completar)_ | _(completar)_ |

## Evaluación crítica
| Hallazgo (verificable) | Criterio | Decisión (Acepto/Adapto/Rechazo) | Justificación propia |
|---|---|---|---|
| `f"... WHERE id = {m}"` puede parecer inyección SQL, pero solo se interpola el marcador (`?`/`%s`); los datos van como parámetros. Probar con `x' OR '1'='1` como correo | Seguridad | _(completar)_ | _(completar)_ |
| En MySQL, `rowcount` de un UPDATE sin cambios es 0; se agregó `client_flag=FOUND_ROWS`. **Verificar en su MySQL** | Coherencia entre motores | _(completar)_ | _(completar)_ |
| `except Exception` en el DAO no oculta el error: hace rollback y re-lanza (`raise`); main captura los específicos | Estabilidad | _(completar)_ | _(completar)_ |
| _(agregue un caso propio: algo que la IA sugirió y ustedes cambiaron o descartaron)_ | | | |

## Declaración
Revisamos, ejecutamos y comprendemos el código entregado. Integrantes: _(nombres)_
