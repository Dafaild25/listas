from app.services import parser_onu, parser_ofac_sdn, parser_ofac_consolidado

PARSER_MAP = {
    'ONU': parser_onu.procesar,
    'OFAC_SDN': parser_ofac_sdn.procesar,
    'OFAC_CONSOLIDADO': parser_ofac_consolidado.procesar
}

def enrutar_parser(tipo: str):
    return PARSER_MAP.get(tipo)
