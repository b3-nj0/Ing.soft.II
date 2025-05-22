from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  
from passlib.context import CryptContext

from config.database import get_db

from schemas.schema_user import UsuarioBase
from service.auth import verify_password, crear_usuario
from sqlalchemy.orm import Session
from models.model_user import Usuario as User

usuario = APIRouter()


# Autenticación con DB
def authenticate_user(usuario: str, password: str, db: Session):
    user = db.query(User).filter(User.usuario == usuario).first()
    if not user:
        return None
    if not verify_password(password, user.contrasena):
        return None
    return user

# Login
@usuario.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    request.session["user"] = user.usuario
    return {"message": f"Bienvenido {user.usuario}"}


@usuario.post("/registro", status_code=201)
def registrar_usuario(usuario_in: UsuarioBase, db: Session = Depends(get_db)):
    try:
        nuevo_usuario = crear_usuario(db, usuario_in)
        return {"mensaje": "Usuario creado correctamente", "id_usuario": nuevo_usuario.id_usuario}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al crear usuario")

# Ruta protegida
@usuario.get("/dashboard")
async def dashboard(request: Request):
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {"message": f"Bienvenido al dashboard, {username}"}

# Logout
@usuario.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Sesión cerrada"}



# Ruta protegida
@usuario.get("/dashboard")
async def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="No autorizado")
    return {"message": f"Acceso concedido a {user}"}

# Logout
@usuario.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Sesión cerrada"}