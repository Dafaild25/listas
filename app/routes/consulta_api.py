from fastapi import APIRouter, Depends, Query, HTTPException
from app.auth.token_auth import validar_token  # Para validar el token
from app.database import SessionLocal
from app.services.fuzzy_search import buscar_fuzzy_general  # Asegúrate de tener la función fuzzy de búsqueda
import sqlite3
import os

router = APIRouter()

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

@router.get("/consultar")
def consultar_persona(
    nombre: str = Query(...),  # El nombre o valor a buscar
    campo: str = Query(...),   # El campo en el que buscar: nombre, alias, nacionalidad, etc.
    user=Depends(validar_token)  # Validamos el token del usuario
):
    """
    Endpoint para consultar personas en las diferentes listas sancionadoras.
    Permite búsqueda fuzzy en las tablas ONO, OFAC SDN, OFAC Consolidado.
    """
    resultados_total = []

    for fuente, tabla in TABLAS.items():
        tabla_extra = None

        if campo != "nombre":
            # Si se busca por alias, nacionalidad o dirección, se usan las tablas adicionales
            tabla_extra = CAMPOS_EXTRA[campo](tabla.replace("persona_", ""))

        resultados = buscar_fuzzy_general(
            nombre_busqueda=nombre,
            campo=campo,
            tabla_persona=tabla,
            tabla_extra=tabla_extra
        )

        for r in resultados:
            # Agregar la fuente a cada resultado para tener la referencia de dónde proviene
            resultados_total.append((*r, fuente))

    resultados_total.sort(key=lambda x: x[2], reverse=True)  # Ordenar por puntuación de coincidencia
    return {"resultados": resultados_total}

