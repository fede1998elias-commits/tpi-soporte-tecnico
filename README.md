# Simulador Chatbot - Soporte Tecnico Nivel 1

TPI - Organizacion Empresarial (UTN). Simulador de un chatbot de Soporte
Tecnico N1 modelado como maquina de estados finitos (FSM). Toma los datos del
usuario por consola, genera un ticket, lo clasifica y lo persiste en SQLite.

## Requisitos previos

- Python 3.6 o superior.
- git (para clonar el repo).
- Nada mas: el simulador usa solo la libreria estandar (incluido `sqlite3`),
  asi que no hay que instalar dependencias ni armar un entorno virtual.

## 1. Clonar el repositorio

```
git clone https://github.com/fede1998elias-commits/tpi-soporte-tecnico.git
cd tpi-soporte-tecnico
```

## 2. Verificar que Python esta instalado

Antes de correr nada, confirmar que Python esta disponible:

```
python --version
```

Tiene que devolver `Python 3.6` o algo mas nuevo. Si no aparece nada o tira
error, probar con `python3 --version`. En Windows, si el comando no se
reconoce, instalar Python desde https://www.python.org/downloads/ y marcar la
opcion "Add Python to PATH" durante la instalacion.

## 3. Ejecutar el simulador

```
python simulador.py
```

(En Linux/Mac puede ser `python3 simulador.py`.)

El programa abre un loop de conversacion por consola. Se responde a cada
pregunta del bot escribiendo en la terminal. Para terminar, escribir `salir`.
Al finalizar un ticket, escribir `nuevo` reinicia el flujo.

## Estados de la FSM

| Estado          | Que espera                  | Transicion                              |
|-----------------|-----------------------------|-----------------------------------------|
| `INICIO`        | (nada)                      | Saluda y pasa a `ESPERA_NOMBRE`.        |
| `ESPERA_NOMBRE` | Nombre completo             | Valida (solo letras, min. 3). OK -> `ESPERA_AREA`. |
| `ESPERA_AREA`   | Area del usuario            | Valida contra la lista. OK -> `ESPERA_DESC`. |
| `ESPERA_DESC`   | Descripcion del problema    | Valida (min. 10 chars). OK -> genera ticket -> `CIERRE`. |
| `CIERRE`        | `nuevo` o cualquier texto   | `nuevo` reinicia a `ESPERA_NOMBRE`.     |

## Reglas de negocio

- **GW1 (validacion de nombre):** rechaza nombres con digitos o de menos de
  3 caracteres.
- **Validacion de area:** debe pertenecer a `RRHH, IT, Finanzas, Logistica, Otro`.
- **Clasificacion automatica:** la categoria se deriva de la descripcion
  (`acceso` -> Acceso, `red` -> Red, resto -> Software).
- **GW2 (prioridad):** las categorias `Acceso` y `Red` escalan a Nivel 2 con
  prioridad `ALTA`; el resto queda en `MEDIA`.

## Casos de error a probar en la demo

1. Nombre invalido: ingresar `Ab` o `Juan123`.
2. Area invalida: ingresar `Marketing`.
3. Descripcion corta: ingresar `falla` (menos de 10 caracteres).

## Estructura del proyecto

- `bot_core.py`: nucleo de la FSM. Define los estados, las validaciones (GW1 y
  GW2), la clasificacion de categoria y la funcion `process_message(sid, texto)`
  que procesa cada mensaje y devuelve la respuesta del bot.
- `simulador.py`: interfaz de consola. Arma el loop de conversacion, lee lo que
  escribe el usuario y se lo pasa al nucleo. No tiene logica de negocio, solo
  entrada/salida.
- `db.py`: capa de persistencia con SQLite. Crea la tabla `tickets`
  (`init_db`) y guarda cada ticket generado (`guardar_ticket`).
- `tickets.db`: base de datos SQLite con los tickets persistidos. No esta
  versionada (se genera sola, ver nota abajo).

## Nota sobre la persistencia

Cada ticket que se genera se guarda en una base SQLite local, en el archivo
`tickets.db`. Ese archivo no viene en el repo: se crea automaticamente la
primera vez que se corre el simulador, por eso esta en el `.gitignore`. Si se
borra, se vuelve a generar vacio en la proxima ejecucion.
