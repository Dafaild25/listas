import sqlite3
from rapidfuzz import fuzz
import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sanciones.db"))


def buscar_fuzzy_general(nombre_busqueda, campo, tabla_persona, tabla_extra=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if tabla_extra:
        query = f"""
            SELECT DISTINCT p.id, p.nombre FROM {tabla_persona} p
            JOIN {tabla_extra} e ON e.persona_id = p.id
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
    else:
        cursor.execute(f"SELECT id, nombre FROM {tabla_persona}")
        resultados = cursor.fetchall()

    conn.close()

    coincidencias = []
    for id_, valor in resultados:
        score = fuzz.partial_ratio(nombre_busqueda.lower(), valor.lower())
        if score >= 75:
            coincidencias.append((id_, valor, score))

    coincidencias.sort(key=lambda x: x[2], reverse=True)  # Ordenar por el puntaje de coincidencia
    return coincidencias
