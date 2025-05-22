from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.service_detalle_pedidos import obtener_top_productos_mas_vendidos
from config.database import get_db
from service.service_ticket_diario import obtener_ventas_del_dia as e
from schemas.schema_venta_dia import VentaDiaResponse
from schemas.schema_ticket import TicketOut


detalle_pedido_route = APIRouter()


@detalle_pedido_route.get("/ventas-del-dia", response_model=List[VentaDiaResponse])
def obtener_ventas_del_dia(db: Session = Depends(get_db)):
    return e(db)

@detalle_pedido_route.get("/top-vendidos")
def top_productos_mas_vendidos(db: Session = Depends(get_db)):
    return obtener_top_productos_mas_vendidos(db)