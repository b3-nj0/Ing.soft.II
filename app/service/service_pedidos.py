from typing import List
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import date
from models.model_ticket import Ticket
from models.model_pedidos import Pedido, EstadoPedido
from models.model_detalles_pedidos import DetallePedido
from schemas.schema_ticket import TicketCreate
from datetime import date
from models.model_producto import Producto
from schemas.schema_pedido import PedidoOut, DetallePedidoOut  # Asegúrate de que los esquemas estén importados

def crear_ticket_con_pedidos(ticket_data: TicketCreate, db: Session) -> Ticket:
    # Obtener el último número de ticket
    ultimo_numero = db.query(func.max(Ticket.numero_ticket)).scalar()
    nuevo_numero = (ultimo_numero or 0) + 1

    # Crear ticket
    nuevo_ticket = Ticket(
        numero_ticket=nuevo_numero,
        descripcion=ticket_data.descripcion
    )
    db.add(nuevo_ticket)
    db.flush()  # Para obtener el id_ticket

    for pedido_data in ticket_data.pedidos:
        nuevo_pedido = Pedido(
            id_ticket=nuevo_ticket.id_ticket,
            estado=pedido_data.estado,
            total=pedido_data.total
        )
        db.add(nuevo_pedido)
        db.flush()  # Para obtener el id_pedido

        for detalle in pedido_data.detalles:
            nuevo_detalle = DetallePedido(
                id_pedido=nuevo_pedido.id_pedido,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal
            )
            db.add(nuevo_detalle)

    db.commit()
    db.refresh(nuevo_ticket)
    return nuevo_ticket






def obtener_pedidos(db: Session):
    # Obtener todos los pedidos
    pedidos = db.query(Pedido).all()
    
    # Convertir los pedidos a su representación Pydantic
    pedidos_serializados = []
    for pedido in pedidos:
        # Obtener los detalles del pedido
        detalles = db.query(DetallePedido).filter(DetallePedido.id_pedido == pedido.id_pedido).all()
        
        # Convertir los detalles a su representación Pydantic
        detalles_serializados = [DetallePedidoOut.model_validate(detalle) for detalle in detalles]
        
        # Verificar el estado y manejar valores inválidos
        estado = pedido.estado if pedido.estado in EstadoPedido.__members__ else EstadoPedido.Pendiente  # Valor por defecto

        # Crear el objeto PedidoOut
        pedido_out = PedidoOut.model_validate({
            "id_pedido": pedido.id_pedido,
            "estado": estado,
            "fecha_hora": pedido.fecha_hora,
            "total": pedido.total,
            "detalles": detalles_serializados
        })
        
        pedidos_serializados.append(pedido_out)
    
    return pedidos_serializados

def obtener_total_ventas_dia(db: Session):
    hoy = date.today()
    total = (
        db.query(func.coalesce(func.sum(Pedido.total), 0))
        .filter(
            Pedido.estado == EstadoPedido.Terminado,
            cast(Pedido.fecha_hora, Date) == hoy
        )
        .scalar()
    )
    return float(total)

def obtener_producto_mas_vendido(db: Session):
    hoy = date.today()
    resultado = (
        db.query(
            Producto.nombre,
            Producto.imagen
        )
        .join(DetallePedido, DetallePedido.id_producto == Producto.id_producto)
        .join(Pedido, Pedido.id_pedido == DetallePedido.id_pedido)
        .filter(
            Pedido.estado == EstadoPedido.Terminado,
            cast(Pedido.fecha_hora, Date) == hoy
        )
        .group_by(Producto.id_producto)
        .order_by(func.sum(DetallePedido.cantidad).desc())
        .first()
    )
    if resultado:
        return {
            "nombre": resultado.nombre,
            "imagen": resultado.imagen
        }
    else:
        return None

def cantidad_ganancia_dia(db: Session):
    hoy = date.today()
    total = (
        db.query(func.coalesce(func.sum(Pedido.total), 0))
        .filter(
            Pedido.estado == EstadoPedido.Terminado,
            cast(Pedido.fecha_hora, Date) == hoy
        )
        .scalar()
    )
    return float(total)

def tabla_pedidos_actuales_por_Aceptar(db: Session):
    pedidos = (
        db.query(Pedido)
        .filter(Pedido.estado == EstadoPedido.EnPreparacion)
        .all()
    )
    return pedidos

def hora_pico_ventas(db: Session, fecha: date):
    resultado = (
        db.query(
            func.hour(Pedido.fecha_hora).label("hora"),
            func.count(Pedido.id_pedido).label("cantidad_ventas")
        )
        .filter(
            Pedido.estado == EstadoPedido.Terminado,
            cast(Pedido.fecha_hora, Date) == fecha
        )
        .group_by(func.hour(Pedido.fecha_hora))
        .order_by(func.count(Pedido.id_pedido).desc())
        .first()
    )
    return resultado

def grafico_ganancias_mes(db: Session, fecha: date):
    resultado = (
        db.query(
            func.month(Pedido.fecha_hora).label("mes"),
            func.sum(Pedido.total).label("ganancia_total")
        )
        .filter(
            Pedido.estado == EstadoPedido.Terminado,
            cast(Pedido.fecha_hora, Date) == fecha
        )
        .group_by(func.month(Pedido.fecha_hora))
        .order_by(func.month(Pedido.fecha_hora))
        .all()
    )
    return resultado

