from fastapi import FastAPI
from app.routes.ingest import router as ingest_router
from app.database import engine, Base
from app.models.fuente import FuenteLista
from app.routes.loguin import router as login_router
from app.routes.consulta_api import router as consulta_router
from app.routes.crear_usuario import router as crear_usuario_router

from app.models.user import Usuario
Base.metadata.create_all(bind=engine)

FuenteLista.__table__.create(bind=engine, checkfirst=True)


app= FastAPI(title="Gestor de listas sancionatorias" )
app.include_router(ingest_router, prefix="/api")


# //consultas
app.include_router(login_router, prefix="/api")
app.include_router(consulta_router, prefix="/api")
#crear usuario
app.include_router(crear_usuario_router, prefix="/api")