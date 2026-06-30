"""
Nucleo del chatbot de Soporte Tecnico Nivel 1.

Implementa la maquina de estados finitos (FSM) del proceso documentado.
Estados: INICIO, ESPERA_NOMBRE, ESPERA_AREA, ESPERA_DESC, CIERRE.
"""

# Estado de cada conversacion identificada por session_id.
sessions = {}  # { session_id: {'state': 'INICIO', 'ticket': {}} }

AREAS = ['RRHH', 'IT', 'Finanzas', 'Logistica', 'Otro']
HIGH_P = ['Acceso', 'Red']  # GW2: estas categorias escalan a N2


def process_message(sid, texto):
    if sid not in sessions:
        sessions[sid] = {'state': 'INICIO', 'ticket': {}}

    s = sessions[sid]
    st = s['state']

    if st == 'INICIO':  # Nodo: Bot saluda
        s['state'] = 'ESPERA_NOMBRE'
        return 'Bienvenido. Ingrese su nombre completo:'

    elif st == 'ESPERA_NOMBRE':  # GW1: validacion de nombre
        # Se rechazan digitos y nombres muy cortos para evitar tickets basura.
        if len(texto.strip()) < 3 or any(c.isdigit() for c in texto):
            return 'ERROR: nombre invalido. Solo letras, minimo 3 caracteres.'
        s['ticket']['nombre'] = texto.strip()
        s['state'] = 'ESPERA_AREA'
        return 'Ingrese su area: ' + ' | '.join(AREAS)

    elif st == 'ESPERA_AREA':
        # Comparacion case-insensitive para aceptar el area en cualquier capitalizacion.
        if texto.strip().upper() not in [a.upper() for a in AREAS]:
            return 'ERROR: area invalida. Opciones: ' + ', '.join(AREAS)
        s['ticket']['area'] = texto.strip()
        s['state'] = 'ESPERA_DESC'
        return 'Describa el problema (minimo 10 caracteres):'

    elif st == 'ESPERA_DESC':
        # Se exige un minimo de detalle para poder clasificar el incidente.
        if len(texto.strip()) < 10:
            return 'ERROR: descripcion demasiado corta. Sea mas especifico.'

        # Clasificacion automatica (regla de negocio)
        cat = 'Acceso' if 'acceso' in texto.lower() else \
              'Red' if 'red' in texto.lower() else 'Software'
        prio = 'ALTA' if cat in HIGH_P else 'MEDIA'  # GW2
        tid = f'TK-{abs(hash(sid)) % 9000 + 1000}'
        s['ticket'].update({'cat': cat, 'prio': prio, 'tid': tid, 'desc': texto.strip()})

        s['state'] = 'CIERRE'
        return (f'Ticket generado: {tid} | Categoria: {cat} | Prioridad: {prio}. '
                f'Un agente lo contactara. Escriba "nuevo" para iniciar otra consulta.')

    elif st == 'CIERRE':
        # Permite reiniciar el flujo sin perder el registro del ticket anterior.
        if texto.strip().lower() == 'nuevo':
            s['state'] = 'ESPERA_NOMBRE'
            s['ticket'] = {}
            return 'Ingrese su nombre completo:'
        return 'Conversacion finalizada. Escriba "nuevo" para iniciar otra consulta.'
