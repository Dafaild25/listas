from fastapi import FastAPI
from app.routes.ingest import router as ingest_router

app= FastAPI(title="Gestor de listas sancionatorias" )
app.include_router(ingest_router, prefix="/api")

