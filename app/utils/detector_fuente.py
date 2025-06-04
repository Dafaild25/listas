import xml.etree.ElementTree as ET

def detectar_fuente(xml_str: str) -> str:
    root = ET.fromstring(xml_str)

    if root.tag == 'CONSOLIDATED_LIST':
        return 'ONU'

    elif root.tag == '{https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML}sdnList':
        ns = {'ofac': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'}
        sdn_entry = root.find('ofac:sdnEntry', ns)

        if sdn_entry is not None:
            # Detectar campos únicos del consolidado
            if sdn_entry.find('ofac:nationalityList', ns) is not None or sdn_entry.find('ofac:placeOfBirthList', ns) is not None:
                return 'OFAC_CONSOLIDADO'
            return 'OFAC_SDN'

    return 'DESCONOCIDO'
