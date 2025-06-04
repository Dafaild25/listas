from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PersonaConsolidado(Base):
    __tablename__ = 'persona_ofac_consolidado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)

    #aqui añadi un campo mas
    fuente_id = Column(Integer, ForeignKey('fuente_lista.id'))
    fuente = relationship("FuenteLista")

    alias = relationship("AliasConsolidado", back_populates="persona", cascade="all, delete-orphan")
    documentos = relationship("DocumentoConsolidado", back_populates="persona", cascade="all, delete-orphan")
    direcciones = relationship("DireccionConsolidado", back_populates="persona", cascade="all, delete-orphan")
    nacionalidades = relationship("NacionalidadConsolidado", back_populates="persona", cascade="all, delete-orphan")

class AliasConsolidado(Base):
    __tablename__ = 'alias_ofac_consolidado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_consolidado.id'))
    persona = relationship("PersonaConsolidado", back_populates="alias")

class DocumentoConsolidado(Base):
    __tablename__ = 'documento_ofac_consolidado'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    numero = Column(String)
    pais_emision = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_consolidado.id'))
    persona = relationship("PersonaConsolidado", back_populates="documentos")

class DireccionConsolidado(Base):
    __tablename__ = 'direccion_ofac_consolidado'
    id = Column(Integer, primary_key=True)
    calle = Column(String)
    ciudad = Column(String)
    provincia = Column(String)
    pais = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_consolidado.id'))
    persona = relationship("PersonaConsolidado", back_populates="direcciones")

class NacionalidadConsolidado(Base):
    __tablename__ = 'nacionalidad_ofac_consolidado'
    id = Column(Integer, primary_key=True)
    nacionalidad = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_consolidado.id'))
    persona = relationship("PersonaConsolidado", back_populates="nacionalidades")
