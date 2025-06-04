# ui/main.py
import streamlit as st
from views import cargar, consultar

st.set_page_config(page_title="Gestor de Sanciones", layout="wide")

st.sidebar.title("🧭 Menú")
opcion = st.sidebar.radio("Ir a:", ["Cargar listas", "Consultar datos"])

if opcion == "Cargar listas":
    cargar.mostrar()
elif opcion == "Consultar datos":
    consultar.mostrar()

