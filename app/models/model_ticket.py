from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.orm import relationship
from config.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket = Column(Integer, primary_key=True, index=True)
    numero_ticket = Column(Integer)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, server_default=func.now())

    pedidos = relationship("Pedido", back_populates="ticket")
