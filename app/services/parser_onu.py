import xml.etree.ElementTree as ET
from app.database import SessionLocal, engine
from app.models import onu

onu.Base.metadata.create_all(bind=engine)

def get_text_any(node, possible_tags):
    for tag in possible_tags:
        val = node.findtext(tag, '').strip()
        if val:
            return val
    return ''

def procesar(xml_str: str, campos: list[str]):
    tree = ET.ElementTree(ET.fromstring(xml_str))
    root = tree.getroot()
    session = SessionLocal()

    # 🔄 Limpiar tablas antes de insertar
    session.query(onu.NacionalidadONU).delete()
    session.query(onu.DireccionONU).delete()
    session.query(onu.DocumentoONU).delete()
    session.query(onu.AliasONU).delete()
    session.query(onu.PersonaONU).delete()
    session.commit()

    count = 0

    for persona in root.findall('.//INDIVIDUAL'):
        nombre = " ".join([
            get_text_any(persona, ['FIRST_NAME', 'NOMBRE']),
            get_text_any(persona, ['SECOND_NAME', 'SEGUNDO_NOMBRE']),
            get_text_any(persona, ['THIRD_NAME', 'TERCER_NOMBRE'])
        ]).strip()

        registro = onu.PersonaONU(nombre=nombre, tipo='Individual')
        session.add(registro)
        session.flush()

        if 'alias' in campos:
            for alias in persona.findall('INDIVIDUAL_ALIAS'):
                nombre_alias = get_text_any(alias, ['ALIAS_NAME', 'NOMBRE_ALIAS'])
                if nombre_alias:
                    session.add(onu.AliasONU(nombre=nombre_alias, persona_id=registro.id))

        if 'documentos' in campos:
            for doc in persona.findall('INDIVIDUAL_DOCUMENT'):
                tipo = doc.findtext('TYPE_OF_DOCUMENT', '').strip()
                numero = doc.findtext('NUMBER', '').strip()
                pais = doc.findtext('ISSUING_COUNTRY', '').strip()
                fecha = doc.findtext('DATE_OF_ISSUE', '').strip()
                nota = doc.findtext('NOTE', '').strip()

                if tipo or numero:
                    session.add(onu.DocumentoONU(
                        tipo=tipo, numero=numero, pais_emision=pais,
                        fecha_emision=fecha, nota=nota, persona_id=registro.id
                    ))

        if 'direcciones' in campos:
            for dir_node in persona.findall('INDIVIDUAL_ADDRESS'):
                calle = dir_node.findtext('STREET', '').strip()
                ciudad = dir_node.findtext('CITY', '').strip()
                provincia = dir_node.findtext('STATE_PROVINCE', '').strip()
                pais = dir_node.findtext('COUNTRY', '').strip()

                if calle or ciudad or provincia or pais:
                    session.add(onu.DireccionONU(
                        calle=calle, ciudad=ciudad, provincia=provincia, pais=pais,
                        persona_id=registro.id
                    ))

        if 'nacionalidades' in campos:
            for n in persona.findall('NATIONALITY/VALUE'):
                if n.text:
                    session.add(onu.NacionalidadONU(
                        nacionalidad=n.text.strip(), persona_id=registro.id
                    ))

        count += 1

    session.commit()
    return f"{count} registros guardados en persona_onu"
