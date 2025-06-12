from app.database import Base  # Ajusta la importación correctamente
from sqlalchemy import Column, Integer, String, DateTime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    expiracion = Column(DateTime)