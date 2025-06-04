from fastapi import APIRouter
from pydantic import BaseModel
import aiohttp
from app.utils.detector_fuente import detectar_fuente
from app.services.parser_router import enrutar_parser

router = APIRouter()

class XMLIngest(BaseModel):
    url: str
    campos: list[str]
    nombre_fuente: str  # ✅ campo nuevo

@router.post("/procesar")
async def procesar_xml(data: XMLIngest):
    async with aiohttp.ClientSession() as session:
        async with session.get(data.url) as resp:
            xml_content = await resp.text()

    tipo_fuente = detectar_fuente(xml_content)
    parser = enrutar_parser(tipo_fuente)

    if not parser:
        return {"error": "Fuente no reconocida"}

    # ✅ se pasa el nombre de la fuente al parser
    resultado = parser(xml_content, data.campos, data.nombre_fuente)
    return {"tipo": tipo_fuente, "resultado": resultado}
