from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session


from config.database import get_db
from schemas.schema_ticket import TicketOut, TicketCreate
from schemas.schema_pedido import OrdenCocinaSchema, EstadoUpdateResponse, PedidoOut
from service.service_pedidos import hora_pico_ventas, ventas_semana
from service.service_pedidos import crear_ticket_con_pedidos, obtener_pedidos, obtener_total_ventas_dia, obtener_producto_mas_vendido, cantidad_ganancia_dia,tabla_pedidos_actuales_por_Aceptar
from service.service_ticket_diario import obtener_ordenes_cocina , cambiar_estado_pedido , cambiar_estado_pedido_cancelado

pedidos_route = APIRouter()



@pedidos_route.post("/pedidos", response_model=TicketOut)
async def crear_ticket(ticket_data: TicketCreate, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    print("JSON recibido:", data)
    print("TicketCreate validado:", ticket_data)
    return crear_ticket_con_pedidos(ticket_data, db)

@pedidos_route.get("/pedidos", response_model=List[PedidoOut])
def obtener_todos_los_pedidos(db: Session = Depends(get_db)):
    return obtener_pedidos(db)

@pedidos_route.get("/ordenes-cocina", response_model=List[OrdenCocinaSchema])
def vista_Coscina(db: Session = Depends(get_db)):
    return obtener_ordenes_cocina(db)

@pedidos_route.put("/ordenes-cocina/{id_pedido}/cambiar-estado", response_model=EstadoUpdateResponse)
def cambiar_estado_cocina(id_pedido = int, db : Session = Depends(get_db)):
    return cambiar_estado_pedido(id_pedido, db)

@pedidos_route.put("/ordenes-cocina/{id_pedido}/cambiar-estado-cancelado", response_model=EstadoUpdateResponse)
def cambiar_estado_cocina(id_pedido = int, db : Session = Depends(get_db)):
    return cambiar_estado_pedido_cancelado(id_pedido, db)

@pedidos_route.get("/total-ventas-dia")
def ventas_dia(db: Session = Depends(get_db)):
    return obtener_total_ventas_dia(db)

@pedidos_route.get("/producto-mas-vendido")
def producto_mas_vendido(db: Session = Depends(get_db)):
    return obtener_producto_mas_vendido(db)

@pedidos_route.get("/ganancia-dia")
def ganancia_dia(db: Session = Depends(get_db)):
    return cantidad_ganancia_dia(db)

@pedidos_route.get("/tabla-pedidos-actuales")
def pedidos_por_Aceptar(db: Session = Depends(get_db)):
    return tabla_pedidos_actuales_por_Aceptar(db)

@pedidos_route.get("/hora-pico-ventas")
def hora_pico(db: Session = Depends(get_db)):
    return hora_pico_ventas(db)

@pedidos_route.get("/ventas/semana")
def obtener_ventas_semana(db: Session = Depends(get_db)):
    return ventas_semana(db)