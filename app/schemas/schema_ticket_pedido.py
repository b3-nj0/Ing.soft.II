from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ItemTicket(BaseModel):
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class TicketImpresion(BaseModel):
    numero_ticket: str  # Formateado con ceros (000123)
    fecha_creacion: str  # Formateada como "22/04/2025 12:58:28"
    descripcion: Optional[str]
    items: List[ItemTicket]
    total: float
    nombre_restaurante: str = "BANDIDOS CHICKEN"
    pie_pagina: str = "BANDIDOS CHICKEN FEXCO"