from fastapi import APIRouter, HTTPException
from app.models.user import Usuario
from app.database import SessionLocal
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

router = APIRouter()

class UsuarioCreate(BaseModel):
    username: str
    password: str

@router.post("/crear_usuario")
async def crear_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    
    # Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter_by(username=usuario.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # Crear un nuevo usuario
    nuevo_usuario = Usuario(
        username=usuario.username,
        password=usuario.password,  # Recuerda que en producción deberías hash la contraseña
        expiracion=datetime.utcnow() + timedelta(hours=24)  # El token será válido por 24 horas
    )
    
    db.add(nuevo_usuario)
    db.commit()
    
    return {"mensaje": f"Usuario {usuario.username} creado exitosamente!"}
