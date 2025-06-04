from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PersonaONU(Base):
    __tablename__ = 'persona_onu'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)
    
    fuente_id = Column(Integer, ForeignKey('fuente_lista.id'))
    fuente = relationship("FuenteLista")

    alias = relationship("AliasONU", back_populates="persona", cascade="all, delete-orphan")
    documentos = relationship("DocumentoONU", back_populates="persona", cascade="all, delete-orphan")
    direcciones = relationship("DireccionONU", back_populates="persona", cascade="all, delete-orphan")
    nacionalidades = relationship("NacionalidadONU", back_populates="persona", cascade="all, delete-orphan")

class AliasONU(Base):
    __tablename__ = 'alias_onu'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_onu.id'))
    persona = relationship("PersonaONU", back_populates="alias")

class DocumentoONU(Base):
    __tablename__ = 'documento_onu'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    numero = Column(String)
    pais_emision = Column(String)
    fecha_emision = Column(String)
    nota = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_onu.id'))
    persona = relationship("PersonaONU", back_populates="documentos")

class DireccionONU(Base):
    __tablename__ = 'direccion_onu'
    id = Column(Integer, primary_key=True)
    calle = Column(String)
    ciudad = Column(String)
    provincia = Column(String)
    pais = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_onu.id'))
    persona = relationship("PersonaONU", back_populates="direcciones")

class NacionalidadONU(Base):
    __tablename__ = 'nacionalidad_onu'
    id = Column(Integer, primary_key=True)
    nacionalidad = Column(String)
    persona_id = Column(Integer, ForeignKey('persona_onu.id'))
    persona = relationship("PersonaONU", back_populates="nacionalidades")
