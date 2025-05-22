from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, DECIMAL, func
from sqlalchemy.orm import relationship
from config.database import Base
import enum

class EstadoPedido(str, enum.Enum):
    Pendiente = "Pendiente"
    EnPreparacion = "En Preparacion"
    Terminado = "Terminado"
    Cancelado = "Cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True)
    id_ticket = Column(Integer, ForeignKey("tickets.id_ticket"))
    estado = Column(Enum(EstadoPedido), default=EstadoPedido.Pendiente)
    fecha_hora = Column(DateTime, server_default=func.now())
    total = Column(DECIMAL(10, 2))

    ticket = relationship("Ticket", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")
