from fastapi import Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy import func, Date, cast
from models.model_ticket import Ticket
from models.model_pedidos import Pedido
from models.model_detalles_pedidos import DetallePedido
from models.model_user import Usuario
from config.database import get_db
from schemas.schema_venta_dia import VentaDiaResponse
from schemas.schema_ticket import TicketOut
from datetime import date, datetime, timedelta


def obtener_usurios(db: Session):
    # Obtener todos los usuarios
    usuarios = db.query(Usuario).all()
    
    # Convertir los usuarios a su representación Pydantic
    return [usuario for usuario in usuarios]

def crear_usuario(db: Session, usuario_data):
    # Generar username y contraseña
    username = Usuario.generar_username(usuario_data.nombre, usuario_data.CI)
    contrasena = Usuario.generar_contrasena()

    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        telefono=usuario_data.telefono,
        direccion=usuario_data.direccion,
        fecha_registro=datetime.now(),
        usuario=username,
        contrasena=contrasena,
        rol=usuario_data.rol,
        CI=usuario_data.CI
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario