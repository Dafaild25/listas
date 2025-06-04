import streamlit as st
from views import cargar, consultar
from views import ConsultaFuzzy

st.set_page_config(page_title="Gestor de Sanciones", layout="wide")

st.sidebar.title("🧭 Menú")
opcion = st.sidebar.radio("Ir a:", ["Cargar listas", "Consultar datos", "Búsqueda inteligente"])

if opcion == "Cargar listas":
    cargar.mostrar()
elif opcion == "Consultar datos":
    consultar.mostrar()
elif opcion == "Búsqueda inteligente":
    ConsultaFuzzy.mostrar_fuzzy()
