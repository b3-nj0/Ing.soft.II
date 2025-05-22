from typing import List
from fastapi import Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session
from config.database import get_db

from models.model_ticket import Ticket
from models.model_pedidos import Pedido
from models.model_detalles_pedidos import DetallePedido
from models.model_producto import Producto


from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import  func, Date, cast
from datetime import  date

from schemas.schema_venta_dia import VentaDiaResponse
from schemas.schema_pedido import OrdenCocinaSchema, EstadoUpdateResponse

def obtener_ventas_del_dia(db: Session = Depends(get_db)):
    hoy = date.today()
    
    try:
        ventas = (
            db.query(
                DetallePedido.id_producto,
                Producto.nombre,
                func.sum(DetallePedido.cantidad).label("cantidad"),
                func.sum(DetallePedido.subtotal).label("total")
            )
            .join(Producto, DetallePedido.id_producto == Producto.id_producto)
            .join(Pedido, DetallePedido.id_pedido == Pedido.id_pedido)
            .join(Ticket, Pedido.id_ticket == Ticket.id_ticket)
            .filter(cast(Ticket.fecha_creacion, Date) == hoy)
            .group_by(DetallePedido.id_producto, Producto.nombre)
            .order_by(func.sum(DetallePedido.cantidad).desc())
            .all()
        )
        
        return [
            VentaDiaResponse(
                id_producto=venta.id_producto,
                nombre=venta.nombre,
                cantidad=venta.cantidad,
                total=float(venta.total)
            ) for venta in ventas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





# Dependency to get DB session



def obtener_ordenes_cocina(db: Session = Depends(get_db)):
    # Querying pedidos joined with detalle_pedidos and productos
    resultados = (
        db.query(
            Pedido.id_pedido.label("numero_ticket"),
            Producto.nombre.label("nombre_plato"),
            DetallePedido.cantidad.label("cantidad"),
            Pedido.estado.label("estado_plato"),
            Pedido.fecha_hora.label("hora"),
        )
        .join(DetallePedido, Pedido.id_pedido == DetallePedido.id_pedido)
        .join(Producto, DetallePedido.id_producto == Producto.id_producto)
        .filter(Pedido.estado.in_(["Pendiente", "En preparación"]))
        .order_by(Pedido.fecha_hora.desc())
        .all()
    )

    # Transform orm results to schema-compatible dicts
    ordenes = []
    for row in resultados:
        ordenes.append(
            OrdenCocinaSchema(
                numero_ticket=row.numero_ticket,
                nombre_plato=row.nombre_plato,
                cantidad=row.cantidad,
                estado_plato=row.estado_plato,
                hora=row.hora.isoformat() if row.hora else None,
            )
        )
    return ordenes





# Pydantic schema for the response






def cambiar_estado_pedido(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Definir ciclo de estados
    ciclo_estados = ["Pendiente", "Terminado", "Cancelado"]

    # Obtener índice actual del estado, si no está en ciclo lo ponemos como inicio "Pendiente"
    try:
        idx_actual = ciclo_estados.index(pedido.estado)
    except ValueError:
        idx_actual = 0

    # Calcular nuevo índice - siguiente estado en el ciclo
    nuevo_idx = (idx_actual + 1) % len(ciclo_estados)
    nuevo_estado = ciclo_estados[nuevo_idx]

    # Actualizar y guardar
    pedido.estado = nuevo_estado
    db.commit()
    db.refresh(pedido)

    return EstadoUpdateResponse(id_pedido=pedido.id_pedido, nuevo_estado=pedido.estado)


def cambiar_estado_pedido_cancelado(id_pedido: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    # Cambiar de "Pendiente" a "Cancelado" directamente
    if pedido.estado == "Pendiente":
        pedido.estado = "Cancelado"
    else:
        raise HTTPException(status_code=400, detail="El estado solo puede cambiar de 'Pendiente' a 'Cancelado'")
    # Actualizar y guardar
    db.commit()
    db.refresh(pedido)
    return EstadoUpdateResponse(id_pedido=pedido.id_pedido, nuevo_estado=pedido.estado)

