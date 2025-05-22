from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .schema_pedido import PedidoOut, PedidoCreate

class TicketOut(BaseModel):
    id_ticket: int
    numero_ticket: int
    descripcion: Optional[str]
    fecha_creacion: datetime
    pedidos: List[PedidoOut]

    class Config:  
        from_attributes = True

class TicketCreate(BaseModel):
    descripcion: Optional[str]
    pedidos: List[PedidoCreate]

class ItemTicket(BaseModel):
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class TicketImpresion(BaseModel):
    numero_ticket: str
    fecha_creacion: str
    descripcion: Optional[str]
    items: List[ItemTicket]
    total: float
