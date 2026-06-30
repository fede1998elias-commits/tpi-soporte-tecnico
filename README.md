# Simulador Chatbot - Soporte Tecnico Nivel 1

TPI - Organizacion Empresarial (UTN). Simulador de un chatbot de Soporte
Tecnico N1 modelado como maquina de estados finitos (FSM).

## Requisitos

- Python 3.6 o superior.
- Sin librerias externas (solo libreria estandar).

## Como correr

```
python simulador.py
```

El programa abre un loop de conversacion por consola. Se responde a cada
pregunta del bot escribiendo en la terminal. Para terminar, escribir `salir`.
Al finalizar un ticket, escribir `nuevo` reinicia el flujo.

## Estructura

- `bot_core.py`: nucleo de la FSM y la funcion `process_message(sid, texto)`.
- `simulador.py`: interfaz de consola que consume el nucleo.

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
