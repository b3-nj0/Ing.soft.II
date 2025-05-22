from sqlalchemy import Column, Integer, String, TIMESTAMP
from config.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    telefono = Column(String(15))
    direccion = Column(String(50))
    fecha_registro = Column(TIMESTAMP)
    usuario = Column(String(15), unique=True)
    contrasena = Column(String(255))
    rol = Column(String(255))
    CI= Column(String(15), unique=True)

