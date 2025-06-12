from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Definir Base antes de la importación de otros modelos
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./sanciones.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


