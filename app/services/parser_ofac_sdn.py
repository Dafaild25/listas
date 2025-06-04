import xml.etree.ElementTree as ET
from app.database import SessionLocal, engine
from app.models import ofac_sdn
from app.models.fuente import FuenteLista

ofac_sdn.Base.metadata.create_all(bind=engine)

def get_text_any(node, possible_tags, ns):
    for tag in possible_tags:
        val = node.findtext(tag, '', namespaces=ns)
        if val:
            return val.strip()
    return ''

def procesar(xml_str: str, campos: list[str], nombre_fuente: str):
    tree = ET.ElementTree(ET.fromstring(xml_str))
    root = tree.getroot()
    ns = {'ofac': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'}

    session = SessionLocal()

    # 🔍 Buscar o crear la fuente
    fuente = session.query(FuenteLista).filter_by(nombre=nombre_fuente).first()
    if not fuente:
        fuente = FuenteLista(nombre=nombre_fuente)
        session.add(fuente)
        session.commit()
        session.refresh(fuente)
    fuente_id = fuente.id

    # 🔄 Eliminar solo registros asociados a esta fuente
    personas = session.query(ofac_sdn.PersonaSDN).filter_by(fuente_id=fuente_id).all()
    for persona in personas:
        session.query(ofac_sdn.NacionalidadSDN).filter_by(persona_id=persona.id).delete()
        session.query(ofac_sdn.DireccionSDN).filter_by(persona_id=persona.id).delete()
        session.query(ofac_sdn.DocumentoSDN).filter_by(persona_id=persona.id).delete()
        session.query(ofac_sdn.AliasSDN).filter_by(persona_id=persona.id).delete()
        session.delete(persona)
    session.commit()

    count = 0

    for entry in root.findall('ofac:sdnEntry', ns):
        nombre = get_text_any(entry, ['ofac:lastName', 'ofac:apellido'], ns)
        tipo = get_text_any(entry, ['ofac:sdnType', 'ofac:tipo'], ns)

        persona = ofac_sdn.PersonaSDN(nombre=nombre, tipo=tipo, fuente_id=fuente_id)
        session.add(persona)
        session.flush()

        if 'alias' in campos:
            for aka in entry.findall('ofac:akaList/ofac:aka', ns):
                alias_val = get_text_any(aka, ['ofac:lastName', 'ofac:apellido'], ns)
                if alias_val:
                    session.add(ofac_sdn.AliasSDN(nombre=alias_val, persona_id=persona.id))

        if 'documentos' in campos:
            for doc in entry.findall('ofac:idList/ofac:id', ns):
                tipo = doc.findtext('ofac:idType', '', namespaces=ns).strip()
                numero = doc.findtext('ofac:idNumber', '', namespaces=ns).strip()
                pais = doc.findtext('ofac:idCountry', '', namespaces=ns).strip()

                if tipo or numero:
                    session.add(ofac_sdn.DocumentoSDN(
                        tipo=tipo, numero=numero, pais_emision=pais, persona_id=persona.id
                    ))

        if 'direcciones' in campos:
            for addr in entry.findall('ofac:addressList/ofac:address', ns):
                calle = addr.findtext('ofac:address1', '', namespaces=ns).strip()
                ciudad = addr.findtext('ofac:city', '', namespaces=ns).strip()
                provincia = addr.findtext('ofac:stateOrProvince', '', namespaces=ns).strip()
                pais = addr.findtext('ofac:country', '', namespaces=ns).strip()

                if calle or ciudad or provincia or pais:
                    session.add(ofac_sdn.DireccionSDN(
                        calle=calle, ciudad=ciudad, provincia=provincia, pais=pais,
                        persona_id=persona.id
                    ))

        if 'nacionalidades' in campos:
            for n in entry.findall('ofac:nationalityList/ofac:nationality/ofac:country', ns):
                if n.text:
                    session.add(ofac_sdn.NacionalidadSDN(
                        nacionalidad=n.text.strip(), persona_id=persona.id
                    ))

        count += 1

    session.commit()
    return f"{count} registros guardados para fuente '{nombre_fuente}'"
