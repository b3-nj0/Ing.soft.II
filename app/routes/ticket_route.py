from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
# from service.service_ticket import generar_ticket_impresion
from service.service_ticket import obtener_ultimo_ticket_para_impresion

from schemas.schema_venta_dia import VentaDiaResponse
from schemas.schema_ticket import TicketOut

ticket_routes = APIRouter()

# @ticket_routes.get("/ticket", response_model=List[VentaDiaResponse])
# def generar_ticket_impresio(db: Session = Depends(get_db)):
#     return generar_ticket_impresion(db)

@ticket_routes.get("/ticket/ultimo/imprimir", response_model=TicketOut  )
def ultimo_ticket_para_imprimir(db: Session = Depends(get_db)):
    return obtener_ultimo_ticket_para_impresion(db)
