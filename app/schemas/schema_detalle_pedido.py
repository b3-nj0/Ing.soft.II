from pydantic import BaseModel
from decimal import Decimal

class DetallePedidoOut(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True
        
class DetallePedidoCreate(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal