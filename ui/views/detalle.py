import streamlit as st
import sqlite3
import pandas as pd

import os
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sanciones.db"))

TABLAS = {
    "ONU": "persona_onu",
    "OFAC SDN": "persona_ofac_sdn",
    "OFAC Consolidado": "persona_ofac_consolidado"
}

def mostrar_detalle(persona_id: int, fuente: str):
    conn = sqlite3.connect(DB_PATH)
    tabla = f"persona_{fuente}"
    persona = pd.read_sql_query(f"SELECT * FROM {tabla} WHERE id = ?", conn, params=(persona_id,))

    if persona.empty:
        st.warning("No se encontró la persona.")
        return

    st.subheader(f"🧾 Detalles de: {persona['nombre'][0]}")
    if 'tipo' in persona.columns:
        st.markdown(f"**Tipo:** {persona['tipo'][0]}")

    # Alias
    alias_tabla = f"alias_{fuente}"
    alias = pd.read_sql_query(f"SELECT nombre FROM {alias_tabla} WHERE persona_id = ?", conn, params=(persona_id,))
    if not alias.empty:
        st.markdown("### 🏷️ Alias")
        st.dataframe(alias)

    # Documentos
    doc_tabla = f"documento_{fuente}"
    if doc_tabla in get_tablas(conn):
        documentos = pd.read_sql_query(f"SELECT * FROM {doc_tabla} WHERE persona_id = ?", conn, params=(persona_id,))
        if not documentos.empty:
            st.markdown("### 📄 Documentos")
            st.dataframe(documentos)

    # Direcciones
    dir_tabla = f"direccion_{fuente}"
    if dir_tabla in get_tablas(conn):
        direcciones = pd.read_sql_query(f"SELECT * FROM {dir_tabla} WHERE persona_id = ?", conn, params=(persona_id,))
        if not direcciones.empty:
            st.markdown("### 🏠 Direcciones")
            st.dataframe(direcciones)

    # Nacionalidades
    nac_tabla = f"nacionalidad_{fuente}"
    if nac_tabla in get_tablas(conn):
        nacionalidades = pd.read_sql_query(f"SELECT * FROM {nac_tabla} WHERE persona_id = ?", conn, params=(persona_id,))
        if not nacionalidades.empty:
            st.markdown("### 🌐 Nacionalidades")
            st.dataframe(nacionalidades)

    conn.close()

def get_tablas(conn):
    tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    return tablas['name'].tolist()
