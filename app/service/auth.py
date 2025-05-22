from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.model_user import Usuario
from schemas.schema_user import UsuarioBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash de contraseñas
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verificación de contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def crear_usuario(db: Session, usuario_in: UsuarioBase):
    # Verificar si el usuario ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.usuario == usuario_in.usuario).first()
    if usuario_existente:
        raise ValueError("El nombre de usuario ya está registrado")
    nuevo_usuario = Usuario(
        nombre=usuario_in.nombre,
        telefono=usuario_in.telefono,
        direccion=usuario_in.direccion,
        usuario=usuario_in.usuario,
        contrasena=hash_password(usuario_in.contrasena)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario
