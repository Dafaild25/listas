from fastapi import Header, HTTPException, Depends
from app.database import SessionLocal
from app.models.user import Usuario
from datetime import datetime, timezone

def validar_token(authorization: str = Header(...)):
    username = authorization.replace("-token", "")
    db = SessionLocal()
    user = db.query(Usuario).filter_by(username=username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Aseguramos que user.expiracion sea aware (con zona horaria)
    if user.expiracion.tzinfo is None:
        user.expiracion = user.expiracion.replace(tzinfo=timezone.utc)

    # Comparamos las fechas, ambas son aware
    if user.expiracion < datetime.utcnow().replace(tzinfo=timezone.utc):
        raise HTTPException(status_code=403, detail="Token inválido o expirado")
    
    return user
