import streamlit as st
import sqlite3
import pandas as pd
from views.detalle import mostrar_detalle
import os
from rapidfuzz import fuzz

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sanciones.db"))

TABLAS = {
    "ONU": "persona_onu",
    "OFAC SDN": "persona_ofac_sdn",
    "OFAC Consolidado": "persona_ofac_consolidado"
}

CAMPOS_EXTRA = {
    "alias": lambda tabla: f"alias_{tabla}",
    "nacionalidad": lambda tabla: f"nacionalidad_{tabla}",
    "direccion": lambda tabla: f"direccion_{tabla}"
}

def buscar_fuzzy_general(nombre_busqueda, campo, tabla_persona, tabla_extra=None, campo_extra=None):
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

    coincidencias.sort(key=lambda x: x[2], reverse=True)
    return coincidencias

def mostrar_fuzzy():
    st.title("🔍 Búsqueda inteligente de sancionados")

    fuente = st.selectbox("Selecciona una fuente", list(TABLAS.keys()) + ["Todas"])
    campo_busqueda = st.selectbox("Buscar en:", ["nombre", "alias", "nacionalidad", "direccion"])
    valor = st.text_input("Valor a buscar (parcial o con errores)")

    if st.button("Buscar"):
        if not valor:
            st.warning("Por favor, introduce un valor para buscar.")
            return

        resultados_total = []

        fuentes = TABLAS.keys() if fuente == "Todas" else [fuente]

        for fuente_actual in fuentes:
            tabla_persona = TABLAS[fuente_actual]
            tabla_extra = None

            if campo_busqueda != "nombre":
                tabla_extra = CAMPOS_EXTRA[campo_busqueda](tabla_persona.replace("persona_", ""))

            resultados = buscar_fuzzy_general(
                nombre_busqueda=valor,
                campo=campo_busqueda,
                tabla_persona=tabla_persona,
                tabla_extra=tabla_extra,
                campo_extra=campo_busqueda
            )

            for r in resultados:
                resultados_total.append((*r, fuente_actual))

        resultados_total.sort(key=lambda x: x[2], reverse=True)
        st.session_state.resultado_fuzzy = resultados_total
        st.session_state.pagina_fuzzy = 0

    if "resultado_fuzzy" in st.session_state and st.session_state.resultado_fuzzy:
        resultados = st.session_state.resultado_fuzzy

        st.markdown("### Resultados similares encontrados:")

        resultados_por_pagina = 10
        total_paginas = (len(resultados) - 1) // resultados_por_pagina + 1

        pagina = st.number_input("Página", min_value=1, max_value=total_paginas, value=st.session_state.get("pagina_fuzzy", 0) + 1)
        st.session_state.pagina_fuzzy = pagina - 1

        inicio = st.session_state.pagina_fuzzy * resultados_por_pagina
        fin = inicio + resultados_por_pagina
        resultados_pagina = resultados[inicio:fin]

        for idx, (id_, valor, score, fuente) in enumerate(resultados_pagina):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🧾 **{valor}**")
                st.caption(f"Coincidencia: {score}% | Fuente: {fuente}")
            with col2:
                if st.button("Ver más", key=f"detalle_fuzzy_{idx}"):
                    st.session_state.seleccionado_fuzzy = id_
                    st.session_state.fuente_actual_fuzzy = fuente

    if "seleccionado_fuzzy" in st.session_state and st.session_state.seleccionado_fuzzy:
        mostrar_detalle(st.session_state.seleccionado_fuzzy, TABLAS[st.session_state.fuente_actual_fuzzy].replace('persona_', ''))
