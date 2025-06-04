from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class FuenteLista(Base):
    __tablename__ = "fuente_lista"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    personas = relationship("PersonaONU", back_populates="fuente")
