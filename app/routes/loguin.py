from fastapi import APIRouter, HTTPException, Form
from app.models.user import Usuario
from app.database import SessionLocal
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(Usuario).filter_by(username=username, password=password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Actualizar expiración
    user.expiracion = datetime.now(timezone.utc) + timedelta(hours=24)

    db.commit()
    return {"token": f"{username}-token", "expira": user.expiracion.isoformat()}
