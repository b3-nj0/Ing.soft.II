from fastapi import Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy import func, Date, cast
from models.model_ticket import Ticket
from models.model_pedidos import Pedido
from models.model_detalles_pedidos import DetallePedido
from models.model_producto import Producto 
from config.database import get_db
from schemas.schema_venta_dia import VentaDiaResponse
from schemas.schema_ticket import TicketOut
from datetime import date, datetime, timedelta

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
    
def obtener_top_productos_mas_vendidos(db: Session, limite: int = 5):
    hoy = date.today()
    inicio_dia = datetime.combine(hoy, datetime.min.time()) 
    fin_dia = datetime.combine(hoy + timedelta(days=1), datetime.min.time())  
    resultados = (
        db.query(
            Producto.nombre.label("nombre"),
            func.sum(DetallePedido.cantidad).label("cantidad_vendida")
        )
        .join(DetallePedido, DetallePedido.id_producto == Producto.id_producto)
        .join(Pedido, Pedido.id_pedido == DetallePedido.id_pedido)
        .filter(Pedido.fecha_hora >= inicio_dia, Pedido.fecha_hora < fin_dia)
        .group_by(Producto.nombre)
        .order_by(func.sum(DetallePedido.cantidad).desc())
        .limit(limite)
        .all()
    )

    colores = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
        "#FF9F40", "#C9CBCF", "#2ecc71", "#e74c3c", "#8e44ad"
    ]

    labels = [r.nombre for r in resultados]
    data = [int(r.cantidad_vendida) for r in resultados]
    backgroundColor = colores[:len(data)]

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Platos más vendidos (Hoy)",
                "data": data,
                "backgroundColor": backgroundColor
            }
        ]
    }