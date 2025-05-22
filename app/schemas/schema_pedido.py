from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum
from decimal import Decimal
from .schema_detalle_pedido import DetallePedidoOut
from .schema_detalle_pedido import DetallePedidoCreate

# Pydantic schema for the response

class OrdenCocinaSchema(BaseModel):
    numero_ticket: int
    nombre_plato: str
    cantidad: int
    estado_plato: str
    hora: str

    class Config:
        from_attributes = True


class EstadoUpdateResponse(BaseModel):
    id_pedido: int
    nuevo_estado: str
    
class EstadoPedido(str, Enum):
    Pendiente = "Pendiente"
    Terminado = "Terminado"
    Cancelado = "Cancelado"

class PedidoOut(BaseModel):
    id_pedido: int
    estado: EstadoPedido
    fecha_hora: datetime  # Este campo es requerido
    total: float
    detalles: List[DetallePedidoOut]

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    estado: EstadoPedido = EstadoPedido.Pendiente
    total: Decimal
    detalles: List[DetallePedidoCreate]