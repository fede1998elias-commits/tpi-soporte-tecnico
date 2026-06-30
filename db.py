"""
Capa de persistencia con SQLite para los tickets de Soporte Tecnico N1.

Usa un unico archivo local tickets.db. La libreria sqlite3 es parte de la
biblioteca estandar, por lo que no requiere instalacion.
"""

import sqlite3
from datetime import datetime

DB_PATH = 'tickets.db'


def init_db():
    """Crea la tabla tickets si todavia no existe. Es idempotente."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS tickets (
                ticket_id   TEXT,
                nombre      TEXT,
                area        TEXT,
                descripcion TEXT,
                categoria   TEXT,
                prioridad   TEXT,
                fecha_hora  TEXT
            )'''
        )
        conn.commit()
    finally:
        conn.close()


def guardar_ticket(ticket_dict):
    """Inserta un ticket. La fecha_hora se sella en el momento de persistir."""
    # El dict de la FSM usa claves abreviadas (tid/cat/prio); se mapean a columnas.
    fila = (
        ticket_dict.get('tid'),
        ticket_dict.get('nombre'),
        ticket_dict.get('area'),
        ticket_dict.get('desc'),
        ticket_dict.get('cat'),
        ticket_dict.get('prio'),
        datetime.now().isoformat(timespec='seconds'),
    )
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            '''INSERT INTO tickets
               (ticket_id, nombre, area, descripcion, categoria, prioridad, fecha_hora)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            fila,
        )
        conn.commit()
    finally:
        conn.close()
