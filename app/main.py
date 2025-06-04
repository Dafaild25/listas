from fastapi import FastAPI
from app.routes.ingest import router as ingest_router
from app.database import engine
from app.models.fuente import FuenteLista

FuenteLista.__table__.create(bind=engine, checkfirst=True)

app= FastAPI(title="Gestor de listas sancionatorias" )
app.include_router(ingest_router, prefix="/api")

