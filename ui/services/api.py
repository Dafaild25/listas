# ui/services/api.py
import requests

API_URL = "http://localhost:8000/api/procesar"

def procesar_xml(url: str, campos: list[str], nombre_fuente: str):
    body = {"url": url, "campos": campos,"nombre_fuente":nombre_fuente}
    try:
        res = requests.post(API_URL, json=body)
        return res.json()
    except Exception as e:
        return {"tipo": "Error", "resultado": str(e)}

