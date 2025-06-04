import streamlit as st
import sqlite3
import pandas as pd
from views.detalle import mostrar_detalle

import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sanciones.db"))


TABLAS = {
    "ONU": "persona_onu",
    "OFAC SDN": "persona_ofac_sdn",
    "OFAC Consolidado": "persona_ofac_consolidado"
}

def mostrar():
    st.title("🔎 Consultar registros sancionados")

    fuente = st.selectbox("Selecciona una fuente", list(TABLAS.keys()))
    nombre = st.text_input("Buscar por nombre (parcial o completo)")
    tipo = st.text_input("Tipo (Individual / Entity)")
    pais = st.text_input("País (en dirección o nacionalidad)")
    alias = st.text_input("Alias")

    if st.button("Buscar"):
        st.session_state.resultado = None
        st.session_state.seleccionado = None
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        base = f"SELECT p.id, p.nombre FROM {TABLAS[fuente]} p"
        if fuente != "ONU":
            base = f"SELECT p.id, p.nombre, p.tipo FROM {TABLAS[fuente]} p"

        filtros = []
        joins = []

        if alias:
            alias_tabla = f"alias_{TABLAS[fuente].replace('persona_', '')}"
            joins.append(f"JOIN {alias_tabla} a ON a.persona_id = p.id")
            filtros.append(f"a.nombre LIKE ?")

        if pais:
            dir_tabla = f"direccion_{TABLAS[fuente].replace('persona_', '')}"
            nac_tabla = f"nacionalidad_{TABLAS[fuente].replace('persona_', '')}"
            joins.append(f"LEFT JOIN {dir_tabla} d ON d.persona_id = p.id")
            joins.append(f"LEFT JOIN {nac_tabla} n ON n.persona_id = p.id")
            filtros.append("(d.pais LIKE ? OR n.nacionalidad LIKE ?)")

        if nombre:
            filtros.append("p.nombre LIKE ?")

        if tipo and fuente != "ONU":
            filtros.append("p.tipo LIKE ?")

        join_sql = " ".join(joins)
        where_sql = " AND ".join(filtros)
        final_query = f"{base} {join_sql}"
        if where_sql:
            final_query += f" WHERE {where_sql}"

        params = []
        if alias:
            params.append(f"%{alias}%")
        if pais:
            params.extend([f"%{pais}%", f"%{pais}%"])
        if nombre:
            params.append(f"%{nombre}%")
        if tipo and fuente != "ONU":
            params.append(f"%{tipo}%")

        df = pd.read_sql_query(final_query, conn, params=params)
        conn.close()

        st.session_state.resultado = df
        st.session_state.fuente_seleccionada = fuente
        st.session_state.pagina = 0

    if "resultado" in st.session_state and st.session_state.resultado is not None:
        df = st.session_state.resultado
        fuente = st.session_state.fuente_seleccionada

        if not df.empty:
            st.markdown("### Resultados:")

            # Paginación
            resultados_por_pagina = 10
            total_paginas = (len(df) - 1) // resultados_por_pagina + 1

            pagina = st.number_input("Página", min_value=1, max_value=total_paginas, value=st.session_state.get("pagina", 0) + 1)
            st.session_state.pagina = pagina - 1

            inicio = st.session_state.pagina * resultados_por_pagina
            fin = inicio + resultados_por_pagina
            df_pagina = df.iloc[inicio:fin]

            for idx, row in df_pagina.iterrows():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"🧾 **{row['nombre']}**")
                    if 'tipo' in row:
                        st.caption(f"Tipo: {row['tipo']}")
                with col2:
                    if st.button("Ver más", key=f"detalle_btn_{idx}"):
                        st.session_state.seleccionado = row['id']
                        st.session_state.fuente_actual = fuente

    if "seleccionado" in st.session_state and st.session_state.seleccionado:
        mostrar_detalle(st.session_state.seleccionado, TABLAS[st.session_state.fuente_actual].replace('persona_', ''))
