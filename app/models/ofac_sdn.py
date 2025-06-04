from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PersonaSDN(Base):
    __tablename__ = 'persona_ofac_sdn'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)

    #aqui añadi un campo mas
    fuente_id = Column(Integer, ForeignKey('fuente_lista.id'))
    fuente = relationship("FuenteLista")


    alias = relationship("AliasSDN", back_populates="persona", cascade="all, delete-orphan")
    documentos = relationship("DocumentoSDN", back_populates="persona", cascade="all, delete-orphan")
    direcciones = relationship("DireccionSDN", back_populates="persona", cascade="all, delete-orphan")
    nacionalidades = relationship("NacionalidadSDN", back_populates="persona", cascade="all, delete-orphan")

class AliasSDN(Base):
    __tablename__ = 'alias_ofac_sdn'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_sdn.id'))
    persona = relationship("PersonaSDN", back_populates="alias")

class DocumentoSDN(Base):
    __tablename__ = 'documento_ofac_sdn'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    numero = Column(String)
    pais_emision = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_sdn.id'))
    persona = relationship("PersonaSDN", back_populates="documentos")

class DireccionSDN(Base):
    __tablename__ = 'direccion_ofac_sdn'
    id = Column(Integer, primary_key=True)
    calle = Column(String)
    ciudad = Column(String)
    provincia = Column(String)
    pais = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_sdn.id'))
    persona = relationship("PersonaSDN", back_populates="direcciones")

class NacionalidadSDN(Base):
    __tablename__ = 'nacionalidad_ofac_sdn'
    id = Column(Integer, primary_key=True)
    nacionalidad = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_ofac_sdn.id'))
    persona = relationship("PersonaSDN", back_populates="nacionalidades")
