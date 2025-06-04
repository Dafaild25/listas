# ui/views/cargar.py
import streamlit as st
from services.api import procesar_xml

def mostrar():
    st.title("📤 Cargar lista XML")

    url = st.text_input("URL del archivo XML")
    campos = st.multiselect(
        "Campos a importar",
        ["alias", "documentos", "direcciones", "nacionalidades"]
    )

    if st.button("Procesar"):
        if not url or not campos:
            st.warning("Completa todos los campos")
        else:
            resultado = procesar_xml(url, campos)
            st.success(f"{resultado['tipo']} → {resultado['resultado']}")

