"""
Simulador interactivo por consola del chatbot de Soporte Tecnico Nivel 1.

Corre un loop de conversacion contra bot_core.process_message manteniendo
una unica sesion. Permite probar el flujo completo y los casos de error
(nombre invalido, area invalida, descripcion corta).

Uso: python simulador.py
"""

import bot_core

SESSION_ID = 'demo-1'


def main():
    print('=== Simulador Soporte Tecnico N1 ===')
    print('Escriba "salir" para terminar.\n')

    # Mensaje inicial: el estado INICIO no consume texto, solo dispara el saludo.
    print('BOT:', bot_core.process_message(SESSION_ID, ''))

    while True:
        try:
            texto = input('USTED: ')
        except (EOFError, KeyboardInterrupt):
            print('\nBOT: Sesion interrumpida.')
            break

        if texto.strip().lower() == 'salir':
            print('BOT: Sesion finalizada.')
            break

        respuesta = bot_core.process_message(SESSION_ID, texto)
        print('BOT:', respuesta)


if __name__ == '__main__':
    main()
