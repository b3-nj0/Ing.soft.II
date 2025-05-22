from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.model_detalles_pedidos import DetallePedido
from models.model_ticket import Ticket
from models.model_pedidos import Pedido


from config.database import get_db
from models.model_producto import Producto
from schemas.schema_ticket import TicketOut, TicketImpresion, ItemTicket




# def generar_ticket_impresion(ticket_db: TicketOut, db: Session) -> TicketImpresion:
#     # Obtener nombres de productos y preparar items
#     items = []
#     total = 0.0
    
#     for pedido in ticket_db.pedidos:
#         for detalle in pedido.detalles:
#             producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
#             nombre_producto = producto.nombre if producto else f"Producto {detalle.id_producto}"
            
#             items.append(ItemTicket(
#                 nombre=nombre_producto,
#                 cantidad=detalle.cantidad,
#                 precio_unitario=float(detalle.precio_unitario),
#                 subtotal=float(detalle.subtotal)
#             ))
            
#             total += float(detalle.subtotal)
    
#     return TicketImpresion(
#         numero_ticket=f"{ticket_db.numero_ticket:06d}",
#         fecha_creacion=ticket_db.fecha_creacion.strftime("%d/%m/%Y %H:%M:%S"),
#         descripcion=ticket_db.descripcion,
#         items=items,
#         total=total
#     )



def obtener_ultimo_ticket_para_impresion(db: Session = Depends(get_db)):
    """
    Endpoint para obtener los datos del último ticket creado para impresión.
    """
    # Obtener el último ticket creado (el de ID más alto)
    ticket = db.query(Ticket).order_by(desc(Ticket.id_ticket)).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="No hay tickets en el sistema")
    
    # Obtener todos los pedidos asociados a este ticket
    pedidos = db.query(Pedido).filter(Pedido.id_ticket == ticket.id_ticket).all()
    
    detalles_por_pedido = {}
    total_general = 0.0
    
    for pedido in pedidos:
        # Obtener los detalles de cada pedido
        detalles_pedido = db.query(DetallePedido).filter(DetallePedido.id_pedido == pedido.id_pedido).all()
        
        detalles_formateados = []
        total_pedido = 0.0
        
        for detalle in detalles_pedido:
            # Obtener información del producto
            producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
            
            detalle_info = {
                "id_producto": detalle.id_producto,
                "nombre_producto": producto.nombre if producto else f"Producto {detalle.id_producto}",  # Cambié "nombre" a "nombre_producto"
                "cantidad": detalle.cantidad,
                "precio_unitario": float(detalle.precio_unitario),
                "subtotal": float(detalle.subtotal)
            }
            
            detalles_formateados.append(detalle_info)
            total_pedido += float(detalle.subtotal)
            total_general += float(detalle.subtotal)
        
        detalles_por_pedido[pedido.id_pedido] = detalles_formateados
    
    return {
        "id_ticket": ticket.id_ticket,
        "numero_ticket": ticket.numero_ticket,
        "descripcion": ticket.descripcion,
        "fecha_creacion": ticket.fecha_creacion,
        "pedidos": [{
            "id_pedido": pedido.id_pedido,
            "estado": pedido.estado,
            "fecha_hora": pedido.fecha_hora,
            "total": float(pedido.total),
            "detalles": detalles_por_pedido[pedido.id_pedido],
        } for pedido in pedidos],
        "total": total_general
    }