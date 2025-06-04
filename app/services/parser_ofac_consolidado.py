import xml.etree.ElementTree as ET
from app.database import SessionLocal, engine
from app.models import ofac_consolidado

ofac_consolidado.Base.metadata.create_all(bind=engine)

def get_text_any(node, possible_tags, ns):
    for tag in possible_tags:
        val = node.findtext(tag, '', namespaces=ns)
        if val:
            return val.strip()
    return ''

def procesar(xml_str: str, campos: list[str]):
    tree = ET.ElementTree(ET.fromstring(xml_str))
    root = tree.getroot()
    ns = {'ofac': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'}

    session = SessionLocal()

    # 🔄 Limpiar tablas antes de insertar
    session.query(ofac_consolidado.NacionalidadConsolidado).delete()
    session.query(ofac_consolidado.DireccionConsolidado).delete()
    session.query(ofac_consolidado.DocumentoConsolidado).delete()
    session.query(ofac_consolidado.AliasConsolidado).delete()
    session.query(ofac_consolidado.PersonaConsolidado).delete()
    session.commit()

    count = 0
    for entry in root.findall('ofac:sdnEntry', ns):
        first = get_text_any(entry, ['ofac:firstName', 'ofac:nombre'], ns)
        last = get_text_any(entry, ['ofac:lastName', 'ofac:apellido'], ns)
        nombre = f"{first} {last}".strip() if first else last
        tipo = get_text_any(entry, ['ofac:sdnType', 'ofac:tipo'], ns)

        persona = ofac_consolidado.PersonaConsolidado(nombre=nombre, tipo=tipo)
        session.add(persona)
        session.flush()

        if 'alias' in campos:
            for aka in entry.findall('ofac:akaList/ofac:aka', ns):
                alias_first = aka.findtext('ofac:firstName', '', namespaces=ns).strip()
                alias_last = aka.findtext('ofac:lastName', '', namespaces=ns).strip()
                alias_val = f"{alias_first} {alias_last}".strip() if alias_first else alias_last
                if alias_val:
                    session.add(ofac_consolidado.AliasConsolidado(nombre=alias_val, persona_id=persona.id))

        if 'documentos' in campos:
            for doc in entry.findall('ofac:idList/ofac:id', ns):
                tipo = doc.findtext('ofac:idType', '', namespaces=ns).strip()
                numero = doc.findtext('ofac:idNumber', '', namespaces=ns).strip()
                pais = doc.findtext('ofac:idCountry', '', namespaces=ns).strip()

                if tipo or numero:
                    session.add(ofac_consolidado.DocumentoConsolidado(
                        tipo=tipo, numero=numero, pais_emision=pais, persona_id=persona.id
                    ))

        if 'direcciones' in campos:
            for addr in entry.findall('ofac:addressList/ofac:address', ns):
                calle = addr.findtext('ofac:address1', '', namespaces=ns).strip()
                ciudad = addr.findtext('ofac:city', '', namespaces=ns).strip()
                provincia = addr.findtext('ofac:stateOrProvince', '', namespaces=ns).strip()
                pais = addr.findtext('ofac:country', '', namespaces=ns).strip()

                if calle or ciudad or provincia or pais:
                    session.add(ofac_consolidado.DireccionConsolidado(
                        calle=calle, ciudad=ciudad, provincia=provincia, pais=pais,
                        persona_id=persona.id
                    ))

        if 'nacionalidades' in campos:
            for n in entry.findall('ofac:nationalityList/ofac:nationality/ofac:country', ns):
                if n.text:
                    session.add(ofac_consolidado.NacionalidadConsolidado(
                        nacionalidad=n.text.strip(), persona_id=persona.id
                    ))

        count += 1

    session.commit()
    return f"{count} registros guardados en persona_ofac_consolidado"
